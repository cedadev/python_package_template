import datetime
from parser import CMMSParser
from github import Github



def review_cmms_content():

    gh = Github()
    repo = gh.get_repo("cedadev/cmms")

    contents = repo.get_contents("yaml_files")

    report = {'yaml_errors': {},
              'yamls_found': len(contents),
              'yamls_failed': [],
              'checker ran at': datetime.datetime.now()}
    num_ok = 0
    num_err = 0
    num_failed = 0

    # produce summary message (when run,
    # how many found,
    # how many passed ok,
    # how many with errors)

    for content in contents[0:2]:
        uuid = content.path.split('/')[1][:-4]

        try:
            cmms_entry = CMMSParser(uuid)

            if cmms_entry.errors:
                report['yaml_errors'][uuid] = cmms_entry.content
                num_err += 1

        except:
            report['yamls_failed'].append(uuid)
            num_failed += 1
        num_ok += 1

    report['number of YAMLs with errors'] = num_err
    report['number of passed YAMLs'] = num_ok
    report['number of failed YAMLs'] = num_failed
    report['checker took'] = (report['checker ran at'] - datetime.datetime.now()).min

    return report

result = review_cmms_content()
print result
