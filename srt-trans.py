from deep_translator import GoogleTranslator
import sys
import statistics
import re


def main(filename, lang):
    tr = GoogleTranslator('en', lang)
    with open(filename, 'r') as subtitle_file:
        res = dict()
        line_count = 1
        trans_num = list()
        trans_list = list()

        for li in subtitle_file:
            res[line_count] = li
            if li[0] not in ([str(x) for x in range(0, 10, 1)] + [' ', '\n']):
                trans_num.append(line_count)
                trans_list.append(li)
            line_count += 1

        # 4000 to ensure that the chunked string will be less than the 5k limit
        # on Google translates API.
        c = 4000 // int(statistics.mean([len(x) for x in trans_list]))
        chunked = [trans_list[i:i + c] for i in range(0, len(trans_list), c)]
        i = 0
        chunk_counter = 1
        for chunk in chunked:
            # Ensures that the minimum amount of requests are sent to
            # Googles servers, both to reduce load on their end, as well as the
            # time it takes to process a subtitle file.
            translations = tr.translate(text='@'.join(chunk)).split('@')
            if len(translations) % len(chunk) == 0:
                print(f'TRANSLATION FOR CHUNK {chunk_counter}'
                      f'/{len(chunked)} OKAY')
            else:
                print(f'TRANSLATION FOR CHUNK {chunk_counter}'
                      f'/{len(chunked)} MISMATCH! OUTPUT WON\'T BE CORRECT!')
            for translation in translations:
                res[trans_num[i]] = translation
                i += 1
            chunk_counter += 1

        base_filename = re.search(r'\w+', filename).group(0)
        export_filename = f'{base_filename}-{lang}.srt'
        with open(export_filename, 'w') as export:
            for val in res:
                export.write(res[val])
            print(f'OUTPUT WRITTEN TO {export_filename}')


if __name__ == '__main__':
    try:
        filename = sys.argv[1]
        lang = sys.argv[2]
    except IndexError:
        raise IndexError('ENTER BOTH A VALID FILENAME AND LANGUAGE')
    try:
        main(filename, lang)
    except KeyboardInterrupt:
        print('User interrupt')
