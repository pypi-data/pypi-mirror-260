"""
Reads a JSON file in the right format, compares it with the current
state of the Tango DB, and generates the set of DB API commands needed
to get to the state described by the file. These commands can also
optionally be run.
"""
from __future__ import absolute_import
from __future__ import print_function

import json
import sys
import time
from optparse import OptionParser
from tempfile import NamedTemporaryFile

import tango
from dsconfig.appending_dict.caseless import CaselessDictionary
from dsconfig.configure import configure
from dsconfig.dump import get_db_data
from dsconfig.filtering import filter_config
from dsconfig.formatting import (CLASSES_LEVELS, SERVERS_LEVELS, load_json,
                                 normalize_config, validate_json,
                                 clean_metadata)
from dsconfig.output import show_actions, get_changes
from dsconfig.tangodb import summarise_calls, get_devices_from_dict
from dsconfig.utils import SUCCESS, ERROR, CONFIG_APPLIED, CONFIG_NOT_APPLIED
from dsconfig.utils import green, red, yellow, progressbar, no_colors
from dsconfig.utils import ObjectWrapper


def prepare_config(config, validate=False, include=False, exclude=False,
                   include_classes=False, exclude_classes=False):
    """
    Do various cleaning and validation, as well as filtering on the config.
    """

    # Normalization - making the config conform to standard
    config = normalize_config(config)

    # remove any metadata at the top level (should we use this for something?)
    config = clean_metadata(config)

    # Optional validation of the JSON file format.
    if validate:
        validate_json(config)

    # filtering
    try:
        if include:
            config["servers"] = filter_config(
                config.get("servers", {}), include, SERVERS_LEVELS)
        if exclude:
            config["servers"] = filter_config(
                config.get("servers", {}), exclude, SERVERS_LEVELS, invert=True)
        if include_classes:
            config["classes"] = filter_config(
                config.get("classes", {}), include_classes, CLASSES_LEVELS)
        if exclude_classes:
            config["classes"] = filter_config(
                config.get("classes", {}), exclude_classes, CLASSES_LEVELS,
                invert=True)
    except ValueError as e:
        print(red("Filter error:\n%s" % e), file=sys.stderr)
        raise RuntimeError(ERROR)

    return config


def apply_config(config, db, write=False, update=False, original=None,
                 nostrictcheck=False, case_sensitive=False, sleep=0, verbose=False,
                 cleanup_protected_props=False):
    """
    Takes a config dict, assumed to be valid.

    Find out the operations needed to get from the current DB state
    to one described by the config. Optionally apply them to the DB
    (by using the --write flag).
    """

    if not any(k in config for k in ("devices", "servers", "classes")):
        raise RuntimeError(ERROR)

    # check if there is anything in the DB that will be changed or removed
    if not original:
        original = get_db_data(db, dservers=True, class_properties=True)
    if "servers" in config:
        devices = CaselessDictionary({
            dev: (srv, inst, cls, alias)
            for srv, inst, cls, dev, alias
            in get_devices_from_dict(config["servers"])
        })
    else:
        devices = CaselessDictionary({})
    orig_devices = CaselessDictionary({
        dev: (srv, inst, cls, alias)
        for srv, inst, cls, dev, alias
        in get_devices_from_dict(original["servers"])
    })
    # Find any new stuff with names that collides with what exists.
    collisions = {}
    for dev, (srv, inst, cls, alias) in devices.items():
        for odev, (osrv, oinst, ocls, oalias) in orig_devices.items():
            if odev.lower() == dev.lower():
                server = "{}/{}".format(srv, inst)
                origserver = "{}/{}".format(osrv, oinst)
                if server.lower() != origserver.lower():
                    collisions.setdefault(origserver, []).append((ocls, dev))

    # Alias collisions
    alias_collisions = set()
    _, result = db.command_inout("DbMySQLSelect", "SELECT alias, name FROM device")
    all_aliases = {
        a.lower(): d.lower()
        for a, d in zip(result[::2], result[1::2])
    }
    new_aliases = {
        alias.lower(): device.lower()
        for device, (_, _, _, alias) in devices.items()
        if alias
    }
    potential_alias_collisions = set(new_aliases) & set(all_aliases)
    for alias in potential_alias_collisions:
        new_dev = new_aliases[alias]
        orig_dev = all_aliases[alias]
        if new_dev != orig_dev:
            alias_collisions.add((alias, orig_dev, new_dev))

    # Aliases to be deleted
    removed_aliases = {
        a: d
        for a, d in all_aliases.items()
        if d in devices.keys() and a not in new_aliases
    }

    # "Fake" database object. We will use it to collect all the database
    # calls needed, and then we can present them regardless of whether
    # they are actually performed.
    wrapper = ObjectWrapper()

    # Remove aliases that are no longer present. We must do it in one go,
    # because doing it in the normal procedure is not safe. Removing aliases
    # is not a "local" operation.
    for alias in removed_aliases:
        wrapper.delete_device_alias(alias)

    # Remove colliding aliases, else we will get errors when creating
    for alias, _, _ in alias_collisions:
        wrapper.delete_device_alias(alias)

    # Get the DB calls needed
    configure(config, original,
              update=update,
              ignore_case=not case_sensitive,
              strict_attr_props=not nostrictcheck,
              db=wrapper, cleanup_protected_props=cleanup_protected_props)
    dbcalls = wrapper.calls

    if write and dbcalls:
        # perform the db operations
        for i, (method, args, kwargs) in enumerate(dbcalls):
            if sleep:
                time.sleep(sleep)
            if verbose:
                progressbar(i, len(dbcalls), 20)
            getattr(db, method)(*args, **kwargs)
        print()

    # Remove empty servers caused by collisions
    empty_servers = set()
    for srvname, devs in list(collisions.items()):
        dev_clss = db.get_device_class_list(srvname)
        if (not dev_clss
            or len(dev_clss) == 2 and dev_clss[1].lower == "dserver"):  # just dserver
            wrapper.delete_server(srvname)
            empty_servers.add(srvname)

    return config, original, dbcalls, collisions, alias_collisions, empty_servers


def show_output(config, original, dbcalls, collisions, alias_collisions, empty_servers,
                show_colors=True, show_input=False, show_output=False,
                show_dbcalls=False, verbose=False, write=False, show_json=False):
    """
    Takes output from the apply_config function and presents it in human
    readable ways.
    """

    if show_input:
        print(json.dumps(config, indent=4))
        return

    # Simple JSON output requested, presumably to be consumed by a script.
    if show_json:
        changes = get_changes(original, dbcalls)
        print(json.dumps(changes, indent=4))
        if dbcalls:
            if write:
                return CONFIG_APPLIED
            else:
                return CONFIG_NOT_APPLIED
        else:
            return SUCCESS

    if not show_colors:
        no_colors()

    # Print out a nice diff
    if verbose:
        show_actions(original, dbcalls)

    # optionally dump some information to stdout
    if show_output:
        print(json.dumps(original, indent=4))

    if show_dbcalls:
        print("Tango database calls:", file=sys.stderr)
        for method, args, kwargs in dbcalls:
            print(method, args, file=sys.stderr)

    # Check for moved devices and remove empty servers
    for srvname, devs in list(collisions.items()):
        if verbose:
            srv, inst = srvname.split("/")
            for cls, dev in devs:
                print(red("MOVED (because of collision):"), dev, file=sys.stderr)
                print("    Server: ", "{}/{}".format(srv, inst), file=sys.stderr)
                print("    Class: ", cls, file=sys.stderr)

    # colliding aliases
    for alias, fromdev, todev in alias_collisions:
        if verbose:
            print(red("MOVED ALIAS (because of collision):"), file=sys.stderr)
            print("    Alias: {}".format(alias), file=sys.stderr)
            print("    Device: {} -> {}".format(fromdev, todev), file=sys.stderr)

    # finally print out a brief summary of what was done
    if dbcalls:
        print()
        print("Summary:", file=sys.stderr)
        print("\n".join(summarise_calls(dbcalls, original)), file=sys.stderr)
        if collisions:
            servers = len(collisions)
            devices = sum(len(devs) for devs in list(collisions.values()))
            print(red("Move %d devices from %d servers." %
                      (devices, servers)), file=sys.stderr)
        if empty_servers and verbose:
            print(red("Removed %d empty servers." % len(empty_servers)), file=sys.stderr)

        if write:
            print(red("\n*** Data was written to the Tango DB ***"), file=sys.stderr)
            with NamedTemporaryFile(prefix="dsconfig-", suffix=".json",
                                    delete=False) as f:
                f.write(json.dumps(original, indent=4).encode())
                print(("The previous DB data was saved to %s" %
                       f.name), file=sys.stderr)
            return CONFIG_APPLIED
        else:
            print(yellow(
                "\n*** Nothing was written to the Tango DB (use -w) ***"), file=sys.stderr)
            return CONFIG_NOT_APPLIED

    else:
        print(green("\n*** No changes needed in Tango DB ***"), file=sys.stderr)
        return SUCCESS


def json_to_tango(options, args):
    """
    Note:
    This used to be one big function that contained all the code above. It was bad as an
    entry point for library code, since it included output and everything. It is now
    instead recommended to use the more specific functions, as needed.
    """
    db = tango.Database()

    if len(args) == 0:
        config = load_json(sys.stdin)
    else:
        json_file = args[0]
        with open(json_file) as f:
            config = load_json(f)

    try:
        config = prepare_config(config)
        if options.dbdata:
            with open(options.dbdata) as f:
                dbdata = json.loads(f.read())
        else:
            dbdata = None
        results = apply_config(config, db, write=options.write, update=options.update,
                               original=dbdata, nostrictcheck=options.nostrictcheck,
                               case_sensitive=options.case_sensitive,
                               cleanup_protected_props=options.cleanup_protected_props,
                               sleep=options.sleep, verbose=options.verbose)
    except RuntimeError as e:
        sys.exit(e.args[0])

    retval = show_output(*results, show_colors=not options.no_colors,
                         show_input=options.input,
                         show_output=options.output, show_dbcalls=options.dbcalls,
                         verbose=options.verbose, write=options.write,
                         show_json=options.json)
    sys.exit(retval)


def main():

    usage = "Usage: %prog [options] JSONFILE"
    parser = OptionParser(usage=usage)

    parser.add_option("-w", "--write", dest="write", action="store_true",
                      help="write to the Tango DB", metavar="WRITE")
    parser.add_option("-u", "--update", dest="update", action="store_true",
                      help="don't remove things, only add/update",
                      metavar="UPDATE")
    parser.add_option("--cleanup-protected-props",
                      default=False, action="store_true",
                      help="Force cleanup of 'protected' properties"),
    parser.add_option("-c", "--case-sensitive", dest="case_sensitive",
                      action="store_true",
                      help=("Don't ignore the case of server, device, "
                            "attribute and property names"),
                      metavar="CASESENSITIVE")
    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose", default=True,
                      help="don't print actions to stderr")
    parser.add_option("-o", "--output", dest="output", action="store_true",
                      help="Output the relevant DB state as JSON.")
    parser.add_option("-p", "--input", dest="input", action="store_true",
                      help="Output the input JSON (after filtering).")
    parser.add_option("-d", "--dbcalls", dest="dbcalls", action="store_true",
                      help="print out all db calls.")
    parser.add_option("-v", "--no-validation", dest="validate", default=True,
                      action="store_false", help=("Skip JSON validation"))
    parser.add_option("-s", "--sleep", dest="sleep", default=0.01,
                      type="float",
                      help=("Number of seconds to sleep between DB calls"))
    parser.add_option("-n", "--no-colors",
                      action="store_true", dest="no_colors", default=False,
                      help="Don't print colored output")
    parser.add_option("-j", "--json", action="store_true",
                      help="Output results as JSON (experimental!)")
    parser.add_option("-i", "--include", dest="include", action="append",
                      help=("Inclusive filter on server configutation"))
    parser.add_option("-x", "--exclude", dest="exclude", action="append",
                      help=("Exclusive filter on server configutation"))
    parser.add_option("-a", "--no-strict-check", dest="nostrictcheck",
                      default=False, action="store_true",
                      help="Disable strick attribute property checking")
    parser.add_option("-I", "--include-classes", dest="include_classes",
                      action="append",
                      help=("Inclusive filter on class configuration"))
    parser.add_option("-X", "--exclude-classes", dest="exclude_classes",
                      action="append",
                      help=("Exclusive filter on class configuration"))

    parser.add_option(
        "-D", "--dbdata",
        help="Read the given file as DB data instead of using the actual DB",
        dest="dbdata")

    options, args = parser.parse_args()

    json_to_tango(options, args)


if __name__ == "__main__":
    main()
