kill -9 $(cat ./tmp/pids/unicorn.pid)
sleep 10
bundle exec unicorn -c /home/showcase/hackathon/glasshack/glasshach_api/config/unicorn.rb -D -E development

