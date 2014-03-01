class CreateUsers < ActiveRecord::Migration
  def change
    create_table :users do |t|
      t.string :fname
      t.string :lname
      t.integer :age
      t.string :gender
      t.string :email
      t.string :face_id
      t.string :from

      t.timestamps
    end
  end
end