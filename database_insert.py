from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item

engine = create_engine('sqlite:///database_tables.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#insert statements here
#Insert Category first
#insert items second

#inserting category "Brush" into Category table
brushes = Category(id = 1, category_name = 'Brushes')
session.add(brushes)
session.commit()

#inserting category "Pencils" into category table
pencils = Category(id = 2, category_name = 'Pencils')
session.add(pencils)
session.commit()

pens = Category(id = 3, category_name = 'Pens')
session.add(pens)
session.commit()

markers = Category(id = 4, category_name = 'Markers')
session.add(markers)
session.commit()

canvases = Category(id =5, category_name = 'Canvases')
session.add(canvases)
session.commit()

paper = Category(id = 6, category_name = 'Paper')
session.add(paper)
session.commit()

ink = Category(id = 7, category_name = 'Ink')
session.add(ink)
session.commit()

sketchbooks = Category(id = 8, category_name = 'Sketchbooks')
session.add(sketchbooks)
session.commit()

books = Category(id = 9, category_name = 'Books')
session.add(books)
session.commit()

pastels = Category(id = 10, category_name = 'Pastels')
session.add(pastels)
session.commit()

#end insertion for category table

#begin insertion for items table

windsor_brushes = Item(id = 1, item_name = "Windsor Brush, size 7", description = "Round brush with a blue handle. This brush uses real horse hair.", category_id = 1)
session.add(windsor_brushes)
session.commit()

windsor_brushes_2 = Item(id = 2, item_name = "Windsor Brush, size 9", description = "Round brush with a blue handle. This brush uses real horse hair.", category_id = 1)
session.add(windsor_brushes_2)
session.commit()

derwent_pencils = Item(id = 3, item_name = "Derwent Pencil set 12", description = "A set of 12 pencils by Derwent. These are really good pencils.", category_id = 2)
session.add(derwent_pencils)
session.commit()

steadler_pencils = Item(id = 4, item_name = "Steadler Pencil set 24", description = "A set of 12 pencils by Steadler. These are great pencils that include an eraser.", category_id = 2)
session.add(steadler_pencils)
session.commit()

kuretake_pens = Item(id = 5, item_name = "Kuretake Fudegoki pen", description = "A brilliant calligraphy pen imported from Japan. Its tip is versatile for fine lines or bold strokes for beautiful letter work.", category_id = 3)
session.add(kuretake_pens)
session.commit()

pentel_pens = Item(id = 6, item_name = "Pentel Ball Point Pen", description = "This ball point pen from Pentel has a 0.7 mm.", category_id = 3)
session.add(pentel_pens)
session.commit()

copic_markers = Item(id = 7, item_name = "Copic Marker set of 4", description = "Copic Markers are high end Japanese markers for illustration or manga work.", category_id = 4)
session.add(copic_markers)
session.commit()

crayola_markers = Item(id = 8, item_name = "Crayola Markers set 24", description = "Crayola markers bring fun to the kids room. This 24 set has a variety of color.", category_id = 4)
session.add(crayola_markers)
session.commit()

mona_canvases = Item(id = 9, item_name = "Mona Lisa Canvases set 2", description = 'These 2 canvases by the Mona Lisa brand are made with high end cotton', category_id = 5)
session.add(mona_canvases)
session.commit()

standard_canvases = Item(id = 10, item_name = "Standard Canvas", description = 'This canvas is 9 x 12 and ideal for students', category_id = 5)
session.add(standard_canvases)
session.commit()

rubens_paper = Item(id = 11, item_name = "Rubens Fine Cotton paper, 24 count", description = 'This pack contains 24 sheets of 9 x 12 Rubens Fine Cotton paper. This can be used with most ink work or calligraphy.', category_id = 6)
session.add(rubens_paper)
session.commit()

dunder_mifflin_paper = Item(id = 12, item_name = "Dunder Mifflin Paper", description = "This paper is mainly served as printer paper, but since this is an art website, it's encouraged to use for doodling, sketching, or making origami.", category_id = 6)
session.add(dunder_mifflin_paper)
session.commit()

speedball_ink = Item(id = 13, item_name = "Speedball Ink, 1 Pint", description = "Speedball ink brings you quality opaque ink.", category_id = 7)
session.add(speedball_ink)
session.commit()

standard_ink = Item(id = 14, item_name = "Standard Ink, 2 ounce", description = "Standard Ink is brings you an economical price and good quality. Use it with nibs or brush pens.", category_id = 7)
session.add(standard_ink)
session.commit()

rubens_sketchbook = Item(id = 15, item_name = "Rubens Sketchbook, 150 page count", description = "The Rubens Sketchbook is a hard bound, elegant, A4 sized, plain paper sketch book. Utilize it for doodling or sketching. It can take inks, watercolors, pencils and charcoal.", category_id = 8)
session.add(rubens_sketchbook)
session.commit()

moleskine_sketchbook = Item(id = 16, item_name = "Moleskine Sketchbook, 170 page count", description = "The Moleskine Sketchbook by Moleskine is a classic leather bound sketchbook. It's a favorite of most artist since it's presentable and the quality of paper is great.", category_id = 8)
session.add(moleskine_sketchbook)
session.commit()

anatomy_book = Item(id = 17, item_name = "Old Masters Anatomy", description = 'Render the human anatomy like the old masters. Learn new techniques by reviewing some sketches by Leonardo Da Vinci, and more, and apply that knowledge to modern ways of interpreting the human body.', category_id = 9)
session.add(anatomy_book)
session.commit()

manga_book = Item(id = 18, item_name = "Tatsunoko Character Design", description = "Want to learn how to design sci-fi characters for comics, manga, anime? Learn by observing the different characters developed by Tatsunoko, a global production company of anime that brought the world Speed Racer.", category_id = 9)
session.add(manga_book)
session.commit()