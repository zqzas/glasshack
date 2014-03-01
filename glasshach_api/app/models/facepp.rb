class Facepp

	def self.call(upload_params,api_path,is_upload)
    if is_upload
      connection = Faraday.new(:url => "https://apicn.faceplusplus.com/v2/") do |f|
        f.request :multipart
        f.adapter :net_http
      end
    else
      connection = Faraday.new(:url => "https://apicn.faceplusplus.com/v2/") 
    end
    upload_params[ :api_key ] = Facepp.api_key
    upload_params[ :api_secret] = Facepp.api_secret
    response = connection.post(api_path,upload_params)
    puts response.body
    result = JSON.parse( response.body )
  end

  def self.api_key
    "d18b494051817dbbdd65b455623f3b85"
  end

  def self.api_secret
    "i3uTsPFbeQHlLiPWv4Ak_R8IRQgTHW2o"
  end
end
