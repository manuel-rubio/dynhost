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
    docroot => '/var/www/dymmer/static',
    wsgi_script_aliases => {'/' => '/var/www/dymmer/dymmer/wsgi.py'},
    aliases => [
        {alias => '/static/', path => '/var/www/dymmer/static/'}
    ]
}

# PostgreSQL: database and role
class postgresql-install {
    include postgresql::lib::devel
    class { 'postgresql::server':
        ipv4acls => ['host all dymmer 127.0.0.1/32 md5'],
    }

    postgresql::server::role { 'dymmer':
        password_hash => postgresql_password('dymmer', 'dymmer2014'),
    }

    postgresql::server::db { 'dymmer':
        user     => 'dymmer',
        password => postgresql_password('dymmer', 'dymmer1234'),
    }
}
class { 'postgresql-install': }

# MySQL: database and root user config
class { 'mysql::server':
    root_password    => 'root',
}

# Dependencies for Django project
class deps {
    package { "libmysqlclient-dev":
        ensure => installed
    }
    python::requirements { '/var/www/dymmer/requirements.txt':
        require => [
            Package['libmysqlclient-dev'],
            Class['postgresql-install'],
        ]
    }
}
class { "deps": }

# Add info to database
class fixtures {
    exec { 'syncdb':
        path => "/usr/local/bin:/usr/bin:/bin",
        cwd => '/var/www/dymmer/',
        command => 'python manage.py syncdb --noinput'
    }
    exec { 'migrate':
        path => "/usr/local/bin:/usr/bin:/bin",
        cwd => '/var/www/dymmer/',
        command => 'python manage.py migrate',
        require => Exec['syncdb']
    }
}
class { 'fixtures':
    require => Class['deps']
}

# Dymmer directory
file { '/home/dymmer':
    ensure => "directory",
    owner => 'www-data',
    recurse => true,
}

# Email server
class {'mailcatcher': 
    smtp_port => 25
}
exec {'mailcatcher-service':
    command => "/usr/local/bin/mailcatcher --smtp-port 25 --http-ip 0.0.0.0",
    require => Class['mailcatcher']
}

