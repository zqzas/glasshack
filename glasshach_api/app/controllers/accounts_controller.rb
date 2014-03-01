class AccountsController < ApplicationController

	def index
		oauth_params = {
				:scope => "profile" ,
				:state => "" ,
				:redirect_uri => "http://#{ request.host_with_port }/accounts/google_callback" ,
				:response_type => "code" ,
				:client_id => Google.GOOGLE_CLIENT_ID ,
				:approval_prompt => "force"
			}
		@google_oauth_path = "https://accounts.google.com/o/oauth2/auth?#{ oauth_params.to_param }"
		@google_oauth_path = "#"
	end

	def register
	end

	def show
		@user = User.find( params[ :id ] )
	end

	def google_callback
		params[ :code ]
		"https://oauth2-login-demo.appspot.com/code?state=/profile&code=4/P7q7W91a-oMsCeLvIaQm6bTrgtp7"
		connection = Faraday.new( :url => "https://oauth2-login-demo.appspot.com/" )
		oauth_params = {
				:code => params[ :code ] ,
				:client_id => Google.GOOGLE_CLIENT_ID ,
				:client_secret => Google.GOOGLE_CLIENT_SECRET ,
				:redirect_uri => "http://#{ request.host_with_port }/accounts/google_callback" ,
				:grant_type => "authorization_code"
			}
		response = connection.post( "/code" , oauth_params )
		puts response.body
		token = JSON.parse( response.body )
	end
end
