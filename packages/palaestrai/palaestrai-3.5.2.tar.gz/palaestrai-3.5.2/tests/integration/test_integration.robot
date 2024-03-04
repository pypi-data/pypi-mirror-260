*** Settings ***
Documentation   Integration Test of Medium Voltage ARL Scenario
...
...             Test All Components in PalaestrAI ecosystem, checking for all sorts
...             of details of the run execution. It does not check for results
...             storage explicitly, but will make sure that all log outputs
...             indicate a safe, successful and complete execution. It test 
...             all steps from generation of experiment run files via ArsenAI
...             and using all harl agents in run files then excution of experiments
...             by PalaestrAI.

Library         String
Library         Process
Library         OperatingSystem

*** Test Cases ***
Generate Experiment Run Files Via ArsenAI
    ${result} =                     Run Process    arsenai    generate   .${/}tests${/}fixtures${/}Classic-ARL-Experiment.yml
    Log Many                        ${result.stdout}    ${result.stderr}
    Should Be Equal As Integers     ${result.rc}    0

Create PalaestrAI Database
    ${result} =                     Run Process    palaestrai    database-create
    Log Many                        ${result.stdout}    ${result.stderr}
    Should Be Equal As Integers     ${result.rc}    0

Run PalaestrAI Experiments
    ${EXPERIMENT_RUN_FILES_PATH}        List Files In Directory    .${/}palaestrai-runfiles    Classic-ARL-Experiment_run-*.yml    absolute
    FOR    ${experiment_file}    IN    @{EXPERIMENT_RUN_FILES_PATH}
        Log Many                        ${experiment_file}
        START PROCESS                   palaestrai       experiment-start       ${experiment_file}      stdout=${TEMPDIR}${/}stdout.txt     stderr=${TEMPDIR}${/}stderr.txt  alias=carl-integrationtest
        ${result} =                     Wait For Process  handle=carl-integrationtest  timeout=30 min  on_timeout=kill
        ${grep_result} =                Run Process     grep  "ERROR\|CRITICAL"  ${TEMPDIR}${/}stdout.txt  stderr=${TEMPDIR}${/}stderr.txt
        Log Many                        ${grep_result.stdout}
        Should Be Equal As Integers     ${result.rc}   0
    END