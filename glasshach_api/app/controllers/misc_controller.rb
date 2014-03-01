class MiscController < ApplicationController

  def facematch
    face_id = Facepp.call( { :img => UploadIO.new( params[ :photo ] , "image/jpeg" ) } , "/detection/detect" , true ) [ "face" ] [ 0 ] [ "face_id" ]
    match_id = Facepp.call( { :key_face_id => face_id, :faceset_name => "hackathon2014" } , "/recognition/search" , false ) [ "candidate" ] [ 0 ] [ "face_id" ] 
    puts match_id 
    user = User.where( :face_id => match_id ).first
    render :text => user.to_json
  end
  
  def facecreate
    face_id = Facepp.call( { :img => UploadIO.new( params[ :photo ] , "image/jpeg" ) } , "/detection/detect" , true ) [ "face" ] [ 0 ] [ "face_id" ]
    User.create( 
        :lname => params[ :lname ] , 
        :fname => params[ :fname ] ,
        :age => params[ :age ].to_i ,
        :gender => params[ :gender ] ,
        :email => params[ :email ] ,
        :face_id => face_id ,
        :from => params[ :from ]
      )
    Facepp.call( { :face_id => face_id , :faceset_name => "hackathon2014" } , "/faceset/add_face" , false )
    Facepp.call( { :faceset_name => "hackathon2014" } , "/train/search" , false )

    render :text => "FUCKXXX"
  end

  def test_upload
    render "misc/test_upload"
  end
end
