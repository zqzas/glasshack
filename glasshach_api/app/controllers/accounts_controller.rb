class AccountsController < ApplicationController

	def index
	end

	def register
	end

	def show
		@user = User.find( params[ :id ] )
	end

end
