class User < ActiveRecord::Base
	attr_accessible :age, :email, :face_id, :fname, :gender, :lname, :from, :avatar_url

end
