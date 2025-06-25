The Mushaf Layout refers to the structured data of pages in any Mushaf (printed copy of the Quran).

Layout data is essential for rendering Mushaf pages in digital applications and tools. QUL provides a Mushaf Layout Tool that allows you to design layouts for any Mushaf. Layout data is then exported as downloadable Sqlite or json files.

To render a Mushaf layout, you'll need the following resources:

Quran script in word by word format, See available Quran scripts
Font compatible with your selected Quran script, See available fonts
And layout data for selected Mushaf, See available mushaf layouts
Surah names, you can download Surah names from Quran metadata resource.
Overview of requird data for rendering Mushaf layout
1- Mushaf layout The exported SQLite database includes a pages table that contains data for each line on a page. The table has the following structure:

Column	Description
page_number	The number of the page in the Mushaf.
line_number	The line number on the page.
line_type	Specifies the type of line, possible value for line_type could be:
ayah:Regular line showing the Quran script.
surah_name: A line with Surah name. You can retrieve the Surah details using the surah_number column.
basmallah: A line displaying "Bismillah".
is_centered	A boolean value indicating whether the text on the line should be center-aligned(true) or fully justified(false).
first_word_id	The ID of the first word on this line.
last_word_id	The ID of the last word on this line.
surah_number	Identifies the Surah displayed on this line.
2- Quran script exported database includes a words table with following columns

Column	Description
word_index	The unique ID for each word. This id is referenced in first_word_id and last_word_id in pages table in mushaf layout db
word_key	Uniq word key in Surah:Ayah format
surah	Surah number
ayah	Ayah number.
text	Word text that you'll need to render.
How to render Mushaf page
To render a page of the Mushaf, follow these general steps:

Query the pages table in the layout SQLite database to retrieve the necessary details for each line on the page (including the page_number, line_number, line_type, etc.).
For each line, based on the line_type, determine the content to render:
If the line_type is surah_name, render the Surah name on this line. surah_number filed contain the surah id you need to render .
If the line_type is ayah, retrieve the words between first_word_id and last_word_id from the words table and render those words in order(or concatenate them to form the single string and render it).
If the line_type is basmallah, display the Bismillah on this line.
Ensure that the text for each line is aligned correctly (centered or justified, align the line based on the is_centered field).
Repeat this process for each line on the page until all lines are rendered.
Sample code and preview:

const SurahNames = {
    1: "الفاتحة"
  }

  const pageData = [
    { line_number: 1, line_type: 'surah_name', is_centered: true, first_word_id: null, last_word_id: null, surah_number: 1 },
    { line_number: 2, line_type: 'ayah',  is_centered: true, first_word_id: 1, last_word_id: 5, surah_number: null },
    { line_number: 3, line_type: 'ayah',  is_centered: true, first_word_id: 6, last_word_id: 10, surah_number: null },
    { line_number: 4, line_type: 'ayah',  is_centered: true, first_word_id: 11, last_word_id: 17, surah_number: null },
    { line_number: 5, line_type: 'ayah',  is_centered: true, first_word_id: 18, last_word_id: 23, surah_number: null },
    { line_number: 6, line_type: 'ayah',  is_centered: true, first_word_id: 24, last_word_id: 29, surah_number: null },
    { line_number: 7, line_type: 'ayah',  is_centered: true, first_word_id: 30, last_word_id: 33, surah_number: null },
    { line_number: 8, line_type: 'ayah',  is_centered: true, first_word_id: 34, last_word_id: 36, surah_number: null }
  ];

  const wordData = {
    "1": "بِسۡمِ",
    "6": "ٱلۡحَمۡدُ",
    "11": "ٱلرَّحۡمَٰنِ",
    "14": "مَٰلِكِ",
    "18": "إِيَّاكَ",
    "23": "ٱهۡدِنَا",
    "27": "صِرَٰطَ",
    "2": "ٱللَّهِ",
    "7": "لِلَّهِ",
    "12": "ٱلرَّحِيمِ",
    "15": "يَوۡمِ",
    "19": "نَعۡبُدُ",
    "24": "ٱلصِّرَٰطَ",
    "28": "ٱلَّذِينَ",
    "3": "ٱلرَّحۡمَٰنِ",
    "8": "رَبِّ",
    "13": "٣",
    "16": "ٱلدِّينِ",
    "20": "وَإِيَّاكَ",
    "25": "ٱلۡمُسۡتَقِيمَ",
    "29": "أَنۡعَمۡتَ",
    "4": "ٱلرَّحِيمِ",
    "9": "ٱلۡعَٰلَمِينَ",
    "17": "٤",
    "21": "نَسۡتَعِينُ",
    "26": "٦",
    "30": "عَلَيۡهِمۡ",
    "5": "١",
    "10": "٢",
    "22": "٥",
    "31": "غَيۡرِ",
    "32": "ٱلۡمَغۡضُوبِ",
    "33": "عَلَيۡهِمۡ",
    "34": "وَلَا",
    "35": "ٱلضَّآلِّينَ",
    "36": "٧"
  }
function getWords(firstWordId, lastWordId) {
    return Object.entries(wordData)
        .map(([key, value]) => ({ id: Number(key), text: value })) // Convert keys to numbers
        .sort((a, b) => a.id - b.id) // Sort by word ID
        .filter(word => word.id >= firstWordId && word.id <= lastWordId) // Filter by range
        .map(word => word.text) // Extract text values
        .join(' ');
}

function getSurahName(number) {
    return `سورۃ ${SurahNames[number]}`;
}

function renderPage() {
    const pageElement = document.getElementById('run-preview');
    pageElement.innerHTML = ''; 
   pageElement.classList.add('qpc-hafs'); // Use QPC Hafs font

    pageData.forEach(line => {
        let lineElement = document.createElement('div');
        lineElement.classList.add('line');

        if (line.is_centered) {
            lineElement.style.textAlign = 'center';
            lineElement.style.display = 'flex';
            lineElement.style.justifyContent = 'center';
        }

        switch (line.line_type) {
            case 'surah_name':
                lineElement.innerHTML = getSurahName(line.surah_number);
                lineElement.classList.add('surah-name');
                break;
            case 'ayah':
                lineElement.innerHTML = `${getWords(line.first_word_id, line.last_word_id)}`;
                lineElement.classList.add('ayah');
                break;
            case 'basmallah':
                lineElement.innerHTML = '﷽';
                lineElement.classList.add('basmallah');
                break;
        }

        pageElement.appendChild(lineElement);
    });
}

  renderPage();


  