#!/usr/bin/expect
set timeout 30

set user omadmin
set pswd shangyoo!@#$

set host [lindex $argv 0]
set command [lrange $argv 1 $argc]

spawn ssh $user@$host $command
expect {
    "yes/no" {
        send "yes\r";exp_continue
    }
    "password:" {
        send "$pswd\n";
    }

}

send_user "excuting $command ....\n"

expect {
    eof {send_user "excute command over!"}
    }
