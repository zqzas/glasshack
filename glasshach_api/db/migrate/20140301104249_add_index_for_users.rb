class AddIndexForUsers < ActiveRecord::Migration
  def change
  	add_index :users, :face_id
  end
end
