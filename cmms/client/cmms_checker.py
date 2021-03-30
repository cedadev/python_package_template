import datetime
import logging
from parser import CMMSParser
from github import Github



def review_cmms_content():

    gh = Github()
    repo = gh.get_repo("cedadev/cmms")

    contents = repo.get_contents("yaml_files")

    start_scan_time = datetime.datetime.now()
    report = {'yaml_errors': {},
              'yamls_found': len(contents),
              'yamls_failed': [],
              'checker ran at': datetime.datetime.strftime(start_scan_time, '%Y-%m-%d %H:%M:%S')}
    num_ok = 0
    num_err = 0
    num_failed = 0

    # produce summary message (when run,
    # how many found,
    # how many passed ok,
    # how many with errors)

    for content in contents:
        uuid = content.path.split('/')[1][:-4]

        try:
            cmms_entry = CMMSParser(uuid)

            if cmms_entry.errors:
                report['yaml_errors'][uuid] = cmms_entry.errors
                num_err += 1

        except:
            report['yamls_failed'].append(uuid)
            num_failed += 1
        else:
            num_ok += 1

    report['number of YAMLs with errors'] = num_err
    report['number of passed YAMLs'] = num_ok
    report['number of failed YAMLs'] = num_failed
    report['checker took'] = "%s seconds"% (datetime.datetime.now() - start_scan_time ).seconds

    return report



if __name__ == '__main__':
    log = logging.getLogger()

    log.info('test')
    result = review_cmms_content()
    print(result)

