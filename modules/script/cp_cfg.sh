#!/usr/bin/expect
set timeout 5
set user omadmin
set pswd shangyoo!@#$
set host [lindex $argv 0]

spawn /usr/bin/ssh $user@$host -C "cp -f /home/AA_server/lua/common/common_config.lua /mnt/server/lua/common/common_config.lua"

expect {
	"yes/no" {send "yes\r";exp_continue}
        "password:" {send $pswd;send "\r";exp_continue}
}
