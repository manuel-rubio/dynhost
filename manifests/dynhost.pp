# -*- mode: ruby -*-
# vi: set ft=ruby :

# Python
class { "python":
    version => 'system',
    dev => true,
    pip => true,
}

# Apache configuration
class { 'apache': 
    default_vhost => false,
}
apache::mod { 'wsgi': }
apache::vhost { 'dymmer.com':
    port => 80,
    docroot => '/var/www/dynhost/static',
    wsgi_script_aliases => {'/' => '/var/www/dynhost/dynhost/wsgi.py'},
    aliases => [
        {alias => '/static/', path => '/var/www/dynhost/static/'}
    ]
}

# PostgreSQL: database and role
class { 'postgresql::server':
    ipv4acls => ['host all dynhost 127.0.0.1/32 md5'],
}

postgresql::server::role { 'dynhost':
    password_hash => postgresql_password('dynhost', 'dynhost2014'),
}

postgresql::server::db { 'ring':
    user     => 'ring',
    password => postgresql_password('ring', 'ring1234'),
}

class pgsql-devel {
    include postgresql::lib::devel
}
class { 'pgsql-devel': }

# MySQL: database and root user config
class { 'mysql::server':
    root_password    => 'root',
}

# Dependencies for Django project
class deps {
    package { "libmysqlclient-dev":
        ensure => installed
    }
    python::requirements { '/var/www/dynhost/requirements.txt':
        require => [
            Package['libmysqlclient-dev'],
            Class['pgsql-devel'],
        ]
    }
}
class { "deps": }

# Add info to database
class fixtures {
    exec { 'syncdb':
        path => "/usr/local/bin:/usr/bin:/bin",
        cwd => '/var/www/dynhost/',
        command => 'python manage.py syncdb --noinput'
    }
    exec { 'migrate':
        path => "/usr/local/bin:/usr/bin:/bin",
        cwd => '/var/www/dynhost/',
        command => 'python manage.py migrate',
    }
    file { 'initial_data.json':
        path => '/vagrant/manifests/initial_data.json'
    }
    exec { 'load data':
        path => "/usr/local/bin:/usr/bin:/bin",
        cwd => '/var/www/dynhost/',
        command => 'python manage.py migrate',
        require => File['initial_data.json'],
    }
}
class { 'fixtures':
    require => Class['deps']
}

# DynHost directory
file { '/home/dynhost':
    ensure => "directory",
    owner => 'www-data',
    recurse => true,
}

# Email server
class {'mailcatcher': 
    smtp_port => 25
}
