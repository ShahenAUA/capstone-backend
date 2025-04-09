make a migration after changes are finalized



animal/pet model:
type/category (dog, cat, parrot, etc.)
breed
age/birth_date
weight
vaccinations (foreign key to vaccination table)
gender/sex
name (optional)
description (optional)

vaccine model:
name
?? add any other necessary fields

vaccination model:
vaccine_id
animal_id
date

shelterprofile model:
profile_id
name
address
description
capacity
registration_number

listing/announcement: (that the animal is available to adopt)
animal_id
listing_date
user_id or shelter_id based on who posted

backlog:
<!-- adoption (to track history records) -->
adoption:
shelter_id
animal_id
date

?? are we going to identify it is the same pet or not
?? maybe just treat each animal as a new entry 