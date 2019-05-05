import os
from flask import Flask, jsonify, request
from symspellpy.symspellpy import SymSpell, Verbosity

app = Flask(__name__)

SYM_SPELL = None

def load_package():
    global SYM_SPELL
    if SYM_SPELL:
        return SYM_SPELL
    max_edit_distance_dictionary = 2
    prefix_length = 7
    
    SYM_SPELL = SymSpell(max_edit_distance_dictionary, prefix_length)
    
    dictionary_path = os.path.join(os.path.dirname(__file__),
                                   "dictionary.txt")
    term_index = 0  
    count_index = 1  
    if not SYM_SPELL.load_dictionary(dictionary_path, term_index, count_index):
        print("Dictionary file not found")
    return SYM_SPELL

@app.route('/spellCorrect', methods=['GET'])
def get_tasks():
    input_term = request.args['input_term']
    correct_words = []
    sym_spell = load_package()
    max_edit_distance_lookup = 2
    
    suggestions = sym_spell.lookup_compound(input_term,
                                            max_edit_distance_lookup)
    for suggestion in suggestions:
        correct_words.append(suggestion.term)
    suggestion_verbosity = Verbosity.CLOSEST  
    suggestions = sym_spell.lookup(input_term, suggestion_verbosity,
                                   max_edit_distance_lookup)
    for suggestion in suggestions:
        if suggestion.term not in correct_words:
            correct_words.append(suggestion.term)
    return jsonify(correct_words)

if __name__ == '__main__':
    app.run(debug=True)

    
