#include <exception>
#include <iostream>
#include <sstream>
#include <string>

#include <CLucene.h>

#include <boost/program_options.hpp>
#include <boost/property_tree/json_parser.hpp>
#include <boost/property_tree/ptree.hpp>


using boost::program_options::options_description;
using boost::program_options::parse_command_line;
using boost::program_options::notify;
using boost::program_options::value;
using boost::program_options::variables_map;
using boost::property_tree::ptree;
using boost::property_tree::read_json;

using lucene::analysis::WhitespaceAnalyzer;
using lucene::document::Document;
using lucene::document::Field;
using lucene::index::IndexWriter;

using std::cerr;
using std::exception;
using std::endl;
using std::ifstream;
using std::stringstream;
using std::string;
using std::wstring;


void IndexJsonFile(const string& fileName, IndexWriter* writer) {
    ifstream in(fileName.c_str());
    for (string line; getline(in, line) && line != string();) {
        try {
            stringstream ss;
            ss << line;
            ptree pt; 
            read_json(ss, pt);

            string title = pt.get_child("title").data();
            wstring wtitle = wstring(title.begin(), title.end());
            Field* field = _CLNEW Field(
                    L"title",
                    wtitle.c_str(),
                    Field::INDEX_TOKENIZED);
            Document document;
            document.add(*field);

            writer->addDocument(&document);
            writer->flush();
        } catch (exception& e) {
            cerr << e.what() << endl;
        }
    }
}


int main(int argc, char** argv) {
    options_description desc("Options");
    desc.add_options()
        ("input_file, i",
         value<string>()->required(),
         "Json-file with data to be indexed")
        ("output_dir, o",
         value<string>()->required(),
         "Directory where to place index");

    variables_map vm;
    store(parse_command_line(argc, argv, desc), vm);
    notify(vm);

    string inputFile = vm["input_file"].as<string>();
    string outputDir = vm["output_dir"].as<string>();

	WhitespaceAnalyzer an;
    IndexWriter* writer = _CLNEW IndexWriter(outputDir.c_str(), &an, true);
    IndexJsonFile(inputFile, writer);
    return 0;
}
