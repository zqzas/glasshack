class MiscController < ApplicationController
def facematch
    face_set = Facepp.call(
        { :url => params[ :photo ] } ,
        "/detection/detect" , false ) [ "face" ]
    image = MiniMagick::Image.open(params[ :photo ])
    
    @result_set = []

    face_set.each do |face|
      face_id = face["face_id"]
      position = face["position"]
      faceImage = MiniMagick::Image.open(params[ :photo ])
      puts faceImage[:width]
      puts faceImage[:height]
      width = (position["width"] * faceImage[:width] / 100).to_i
      height = (position["height"] * faceImage[:height] / 100).to_i
      x = (position["center"]["x"] * faceImage[:width] / 100).to_i - width / 2
      y = (position["center"]["y"] * faceImage[:height] / 100).to_i - height / 2
      crop_params = "#{width}x#{height}+#{x}+#{y}"
      puts crop_params
      faceImage.crop(crop_params)
      faceImage.write("./public/image/#{face_id}.jpg")

      match_candidate = Facepp.call( 
         { :key_face_id => face_id, :faceset_name => "hackathon2014" } ,
         "/recognition/search" , false ) [ "candidate" ]  [ 0 ]
      if match_candidate[ "similarity" ] > 80
        hash = JSON.parse(User.where( :face_id => match_candidate[ "face_id" ] ).first.to_json).symbolize_keys
        hash[:img] = "/image/#{face_id}.jpg"
        @result_set << hash
      else
        low = face["attribute"]["age"]["value"] - face["attribute"]["age"]["range"]
        high = face["attribute"]["age"]["value"] + face["attribute"]["age"]["range"]
        @result_set <<{
        :age => "#{low} - #{high}",
        :gender => face["attribute"]["gender"]["value"] ,
        :img => "/image/#{face_id}.jpg"}
      end
    end

    render "misc/timeline", :layout => false 
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
