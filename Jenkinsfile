pipeline {
  agent any
  stages {
    stage('check_src') {
      parallel {
        stage('check_src') {
          steps {
            sh 'echo "check src"'
            sh 'ip a'
          }
        }
        stage('check hardware') {
          steps {
            git(url: 'git@github.com:farnsford/rpmbuild.git', branch: 'master', changelog: true)
          }
        }
      }
    }
    stage('build') {
      steps {
        sh 'rpmbuild -ba'
      }
    }
  }
}