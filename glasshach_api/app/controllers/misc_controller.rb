class MiscController < ApplicationController

  def facematch
    face_id = Facepp.call( { :img => params[ :photo ] } , "/detection/detect" ) [ "face" ] [ 0 ] [ "face_id" ]
    match_id = Facepp.call( { :key_face_id => face_id, :faceset_name => "hackthon2014"}, "/recognition/search")
    render :text => face_id
  end
  
  def facecreate
    face_id = Facepp.call( { :img => params[ :photo ] } , "/detection/detect" ) [ "face" ] [ 0 ] [ "face_id" ]
    Facepp.call( { :face_id => face_id , :faceset_name => "hackthon2014" } , "/faceset/add_face" )
    Facepp.call( { :face_name => "hackthon2014" } , "/train/search")
  end
end
