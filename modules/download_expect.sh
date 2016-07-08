#!/usr/bin/expect
set timeout 10

set user omadmin
set pswd shangyoo!@#$

set filename [lindex $argv 0]
set host_path [lindex $argv 1]

spawn scp $filename $user@$host_path 
expect {
    "yes/no" {
        send "yes\r";exp_continue
    }
    "password:" {
        send "$pswd\n";
    }

}

expect {
    "100%" {sleep 1}
    "%" {exp_continue}
    timeout {exit 1}
    }

expect eof {send_user "it's ok"}
