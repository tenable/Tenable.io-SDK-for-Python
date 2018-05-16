@Library('tenable.common@v1.0.0')
import com.tenable.jenkins.*
import com.tenable.jenkins.builds.*
import com.tenable.jenkins.builds.checkmarx.*
import com.tenable.jenkins.builds.nexusiq.*
import com.tenable.jenkins.builds.onprem.*
import com.tenable.jenkins.common.*
import com.tenable.jenkins.deployments.*
import com.tenable.jenkins.msg.*
import com.tenable.jenkins.slack2.Slack

def projectProperties = [
    [$class: 'BuildDiscarderProperty',strategy: [$class: 'LogRotator', numToKeepStr: '5']],
    disableConcurrentBuilds(),
    [$class: 'ParametersDefinitionProperty', parameterDefinitions:
        [[$class: 'StringParameterDefinition', defaultValue: 'io/qa-milestone', description: '', name: 'SITE_BRANCH']]]
]

properties(projectProperties)

Common common = new Common(this)
BuildsCommon buildsCommon = new BuildsCommon(this)

try {
    node(Constants.DOCKERNODE) {
        buildsCommon.cleanup()

        stage('scm auto') {
            dir('tenableio-sdk') {
                checkout scm
            }
            dir('automation') {
                git(branch:'develop',
                    changelog:false,
                    credentialsId: Constants.BITBUCKETUSER,
                    poll:false,
                    url:'ssh://git@stash.corp.tenablesecurity.com:7999/aut/automation-tenableio.git')
            }
            dir('site') {
                git(branch:params.SITE_BRANCH,
                    changelog:false,
                    credentialsId: Constants.BITBUCKETUSER,
                    poll:false,
                    url:'ssh://git@stash.corp.tenablesecurity.com:7999/aut/site-configs.git')
            }
        }

        docker.withRegistry(Constants.AWS_DOCKER_REGISTRY) {
            docker.image(Constants.DOCKER_CI_VULNAUTOMATION_BASE).inside('-u root') {
                stage('build auto') {
                    buildsCommon.prepareGit()

                    sshagent([Constants.BITBUCKETUSER]) {
                        timeout(time: 24, unit: Constants.HOURS) {
                            try {
                                sh '''
                                cd automation || exit 1
                                export JENKINS_NODE_COOKIE=
                                unset JENKINS_NODE_COOKIE

                                python3 autosetup.py catium --all --no-venv 2>&1

                                export PYTHONHASHSEED=0
                                export PYTHONPATH=.
                                export CAT_USE_GRID=true

                                python3 tenableio/commandline/sdk_test_container.py --create_container --python --agents 5

                                cd ../tenableio-sdk || exit 1
                                pip3 install -r requirements.txt || exit 1
                                py.test tests --junitxml=test-results-junit.xml || exit 1
                                '''.stripIndent()
                            }
                            finally {
	                           step([$class: 'JUnitResultArchiver', testResults: 'tenableio-sdk/*.xml'])
                            }
                        }
                    }
                }
            }
        }

    common.setResultIfNotSet(Constants.JSUCCESS)
    } 
}
catch (ex) {
    common.logException(ex)
    common.setResultAbortedOrFailure()
}
finally {
    common.setResultIfNotSet(Constants.JFAILURE)

    String auser = common.getAbortingUsername()
    String tests = common.getTestResults()
    String took  = '\nTook: ' + common.getDuration()

    Slack slack = new Slack(this)

    messageAttachment = slack.helper.getDecoratedFinishMsg(
        'Tenable SDK Python build finished with result: ',
        "Built off branch ${env.BRANCH_NAME}" + tests + took + auser)
    messageAttachment.channel = '#sdk'

    slack.postMessage(messageAttachment)
}
