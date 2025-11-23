This is the my college python project on professor review(rating) and analysis . 
It consist of feature to add professor, rate(on different matric),edit rating,show rating,graph,compare feature(best feature).
LIBRARIES Used in the projectare:
json: For reading and writing professor data to a file in JSON format.
os: For file path handling and atomic file replacement.
tempfile: To safely write temporary files when saving data.
matplotlib.pyplot: For plotting graphs of professor ratings.
numpy: For array handling and plotting comparisons with bar charts.

FUNCTIONS Used in the program.
load_data(): Initializes the professors dictionary, wrongly tries to clear the data file.
save_data(): Saves the current professors data in a JSON file safely using a temporary file.
add_professor(): Adds a new professor with empty ratings and no subject.
rate_professor(): Adds ratings for teaching, evaluation, internals, and behavior, and calculates overall score.
edit_rating(): Allows editing subject and individual ratings of an existing professor.
display_professors(): Shows all professors with average and detailed ratings.
plot_ratings_graph(): Displays a bar graph of all professors' average overall ratings.
compare_professors(): Compares two professors side-by-side across all rating metrics with a bar chart.
