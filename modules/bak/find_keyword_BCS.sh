#!/usr/bin/expect
set timeout 30

set user omadmin
set pswd shangyoo!@#$

set host [lindex $argv 0]
set log_path [lindex $argv 1]
set key_word [lrange $argv 2 $argc]

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
    "omadmin@" {send "tail -n200 -f $log_path\r";}
    }

expect {
    "$key_word" {send "\003";send "exit\r";exit 0}
    timeout {exit 1}
    eof {exit 1}
    }

