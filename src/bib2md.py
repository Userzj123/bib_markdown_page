from pybtex.database.input import bibtex
import argparse
import datetime
from pathlib import Path
from journal_abbr import find_abb_wiki

CITE_TYPE = ["article",
             "incollection",
             "book"
             ]

source_path = Path(__file__).resolve()
source_dir = source_path.parent
header = Path(str(source_dir) + '/header.txt').read_text()

def main(args):
    # Test arguments
    # args.bib = '/Users/user/Documents/Projects/ERI/ERI.bib'
    # args.output = '/Users/user/Documents/Projects/ERI/reference.md'
    
    parser = bibtex.Parser()
    bib_data = parser.parse_file(args.bib)
    with open(args.output, "w+") as f:
        # f.write(header)
        f.write("# Reference")
        f.write('Generated bibliography markdown file. \nData: '+str( datetime.datetime.now()))
        i = 0
        
        
        # Unordered List
        # f.write('<ul>')
        for label in bib_data.entries:
            i =+ 1
            
            # Unordered List Item
            # f.write('<li>')
            f.write('\n- ')
            # f.write(' <span style="font-family: sans">')
            
            # anchor
            f.write('<a name="%s"></a> ' % (label))
            
            # Author list
            author_list = ''
            comma_i = 0
            middle_string = ', '
            end_string = '., '
            for au in bib_data.entries[label].persons['author']:
                comma_i += 1
                if comma_i == len(bib_data.entries[label].persons['author'])-1:
                    end_string = '. and '
                elif comma_i == len(bib_data.entries[label].persons['author']):
                    end_string = '.'
                author_list += au.last_names[0] + middle_string
                if len(au.middle_names)!= 0: author_list += (au.middle_names[0].replace(' ', ''))[0].capitalize()+ '. '
                author_list += au.first_names[0][0] + end_string
                
                # Replace acute and uml letter
                
                ind_acute = author_list.rfind("{\\\'")
                ind_uml = author_list.rfind('{\\\"')
                if ind_acute != -1:
                    replace_term = 'acute'
                    # Not recognize by github
                    # author_list = author_list[:ind_acute-1] + '&'  + author_list[ind_acute+3] + replace_term + author_list[ind_acute+6:]
                    author_list = author_list[:ind_acute-1] +  author_list[ind_acute+3] + author_list[ind_acute+6:]
                elif ind_uml != -1:
                    replace_term = 'uml'
                    # author_list = author_list[:ind_uml-1] + '&'  + author_list[ind_uml+3] + replace_term + author_list[ind_uml+6:]
                    author_list = author_list[:ind_uml-1] + author_list[ind_uml+3] + author_list[ind_uml+6:]
                
                author_list = author_list.replace('{', '')
                author_list = author_list.replace('}', '')
                
                # print(author_list)

            
            f.write('<span style="font-variant: small-caps"> %s </span>' % author_list)
            
            # Year
            assert 'year' in bib_data.entries[label].fields.keys()
            f.write(' %s ' % (bib_data.entries[label].fields['year']))
            
            # Article Title
            if 'doi' in bib_data.entries[label].fields.keys():
                f.write(' <a href="https://doi.org/%s"> %s. </a>' % (bib_data.entries[label].fields['doi'], bib_data.entries[label].fields['title'].replace('{', '').replace('}', '')))
            else:
                f.write(' %s.' % (bib_data.entries[label].fields['title'].replace('{', '').replace('}', '').replace('\\', '')))
            
            # Journal abbr
            # name
            assert bib_data.entries[label].type in CITE_TYPE
            if bib_data.entries[label].type == 'incollection':
                f.write(' <i> %s</i>' % bib_data.entries[label].fields['booktitle'].replace('{', '').replace('}', '').replace('\\', ''))
            elif bib_data.entries[label].type == 'article':
                journal_name = bib_data.entries[label].fields['journal'].replace('{', '').replace('}', '').replace('\\', '')
                try: journal_name = find_abb_wiki(journal_name)
                except: print(journal_name + " cannot find abbreviation")
                f.write(' <i> %s</i>' % journal_name)
            elif bib_data.entries[label].type == 'book':
                f.write(' <i> %s</i>' % bib_data.entries[label].fields['title'].replace('{', '').replace('}', '').replace('\\', ''))
            
            # Volume
            if 'volume' in bib_data.entries[label].fields.keys():
                f.write(' <b> %s </b>' % bib_data.entries[label].fields['volume'])
                
            # Issue
            if 'number' in bib_data.entries[label].fields.keys(): 
                f.write(' (%s)' % bib_data.entries[label].fields['number'])
            

            # Page
            if 'page' in bib_data.entries[label].fields.keys():
                f.write(', %s' % bib_data.entries[label].fields['pages'])
            
            
            # f.write('</li>\n')
            
            # f.write('</span>\n')
            f.write('\n')
            
        # f.write('\n</ul>\n')

            
        
        


if __name__ == "__main__":

    # Parse the input arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--bib', type=str, default='./main.bib',
                        help='Specify the bib file that you want to run')
    parser.add_argument('--output', type=str, default='./reference.md',
                        help='Specify the markdown file that you want to output')
    args = parser.parse_args()
    main(args)
