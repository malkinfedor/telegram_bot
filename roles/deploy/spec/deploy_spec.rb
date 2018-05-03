require '/tmp/kitchen/spec/spec_helper.rb'


describe file('/etc/yum.repos.d/epel.repo') do
  it { should exist }
  it { should contain "https://mirrors.fedoraproject.org/metalink?repo=epel-7&arch=$basearch" }
end

describe package( 'python34' ) do
    it { should be_installed }
end

describe package( 'python34-setuptools' ) do
    it { should be_installed }
end

describe package( 'python-virtualenv' ) do
    it { should be_installed }
end

describe package( 'git' ) do
    it { should be_installed }
end

describe file('/usr/bin/pip3') do
  it { should exist }
end

describe file('/opt/telegram-bot') do
  it { should exist }
end

describe file('/opt/telegram-bot/env') do
  it { should exist }
end

describe file('/opt/telegram-bot/bot.sh') do
  it { should exist }
end

describe file('/opt/telegram-bot/bot_tests.sh') do
  it { should exist }
end

describe service('telegram-bot') do
  it { should be_enabled   }
  it { should be_running   }
end

