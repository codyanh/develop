#!/usr/bin/expect
set timeout 30

set user omadmin
set pswd shangyoo!@#$

set host [lindex $argv 1]
set ser_name [lindex $argv 0]

spawn ssh $user@$host 
expect {
    "yes/no" {
        send "yes\r";exp_continue
    }
    "password:" {
        send "$pswd\n";
    }

}

expect {
    "omadmin@" {send "echo PID:`pidof $ser_name`";send "\n"; send "exit\n"}
    }


expect {
    close {exit 0}
    eof {exit 0}
    }
