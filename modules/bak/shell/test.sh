#!/usr/bin/expect
set timeout 300

set user omadmin
set host [lindex $argv 0]
set pswd shangyoo!@#$

spawn ssh omadmin@192.168.223.1
expect {
    "yes/no" {
        send "yes\r";exp_continue
    }
    "password:" {
        send "$pswd\n";
    }

}
expect {
    "*Last login*" {send "touch /home/omadmin/aa.txt\n"}
}

expect {
    eof {send_user "eof"}
    }
