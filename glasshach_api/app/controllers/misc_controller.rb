class MiscController < ApplicationController

  def facematch
    face_set = Facepp.call(
        { :img => Faraday::UploadIO.new( params[ :photo ] , "image/jpeg" ) } ,
        "/detection/detect" , true ) [ "face" ]
    
    result_set = []

    face_set.each do |face|
      face_id = face["face_id"]
      match_candidate = Facepp.call( 
         { :key_face_id => face_id, :faceset_name => "hackathon2014" } ,
         "/recognition/search" , false ) [ "candidate" ]  [ 0 ]
      if match_candidate[ "similarity" ] > 80
        hash = User.where( :face_id => match_candidate[ "face_id" ] ).first.to_a
        hash[:img] = ""
        result_set = result_set << hash
      else
        result_set = result_set <<
        {:age => "#{face["attribute"]["age"]["value"]}+-#{face["attribute"]["age"]["range"]}",
         :gender => face["attribute"]["gender"] ,
         :img => ""
        }
      end
    end

    render :text => result_set.to_json
  end
  
  def facecreate
    face_id = Facepp.call( 
        { :img => Faraday::UploadIO.new( params[ :photo ] , "image/jpeg" ) } ,
        "/detection/detect" , true ) [ "face" ] [ 0 ] [ "face_id" ]
    User.create( 
        :lname => params[ :lname ] , 
        :fname => params[ :fname ] ,
        :age => params[ :age ].to_i ,
        :gender => params[ :gender ] ,
        :email => params[ :email ] ,
        :face_id => face_id ,
        :from => params[ :from ]
      )
    res = Facepp.call( 
        { :face_id => face_id , :faceset_name => "hackathon2014" } ,
        "/faceset/add_face" , false )
    if res[ "success" ]
      Facepp.call( { :faceset_name => "hackathon2014" } , "/train/search" , false )
    end

    render :text => "FUCKXXX"
  end

  def test_upload
    render "misc/test_upload"
  end
end
