class AccountsController < ApplicationController

	def index
		oauth_params = {
				:scope => "https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/plus.login https://www.googleapis.com/auth/userinfo.email" ,
				:state => "" ,
				:redirect_uri => "http://#{ request.host_with_port }/accounts/google_callback" ,
				:response_type => "code" ,
				:client_id => Google.GOOGLE_CLIENT_ID ,
				:approval_prompt => "force"
			}
		@google_oauth_path = "https://accounts.google.com/o/oauth2/auth?#{ oauth_params.to_param }"
	end

	def register
	end

	def show
		@user = User.find( params[ :id ] )
	end

	def google_callback
		connection = Faraday.new( :url => "https://accounts.google.com/" )
		oauth_params = {
				:code => params[ :code ] ,
				:client_id => Google.GOOGLE_CLIENT_ID ,
				:client_secret => Google.GOOGLE_CLIENT_SECRET ,
				:redirect_uri => "http://#{ request.host_with_port }/accounts/google_callback" ,
				:grant_type => "authorization_code"
			}
		response = connection.post( "/o/oauth2/token" , oauth_params )
		puts "[GOOGLE OAUTH LOGIN]"
		puts response.body
		token = JSON.parse( response.body )

		connection2 = Faraday.new( :url => "https://www.googleapis.com/" )
		response2 = connection2.get( "/plus/v1/people/me" , { :access_token => token[ "access_token" ] } )

		pinfo = JSON.parse( response2.body )

		redirect_params = {
				:fname => pinfo[ "name" ] [ "givenName" ] ,
				:lname => pinfo[ "name" ] [ "familyName" ] ,
				:gender => pinfo[ "gender" ] ,
				:email => pinfo[ "emails" ] [ 0 ] [ "value" ] ,
				:age => pinfo[ "ageRange" ] [ "min" ] 
			}

		redirect_to( "/accounts/register?#{ redirect_params.to_param }" )
	end
end
