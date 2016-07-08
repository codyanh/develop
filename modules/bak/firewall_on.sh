#!/usr/bin/expect
set timeout 30

set user root
set pswd syyx_REW_&*(

set host [lindex $argv 0]

spawn ssh $user@$host iptables-restore  \<  /etc/firewall_rules && iptables -vnL
expect {
    "yes/no" {
        send "yes\r";exp_continue
    }
    "password:" {
        send "$pswd\n";
    }

}

expect {
    eof {exit 0 }
    timeout {exit 1}
    }
