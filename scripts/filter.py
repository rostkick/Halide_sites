from biopandas.pdb import PandasPdb
import re
import os
import argparse
import sys


def filter(): 

  with open(args.output_info, 'a') as w:
       w.write(f'{header}!{resolution}!{model_name}\n')

  with open(args.output_info, 'r') as f:
    global base_list
    base_list=[]
    text=f.readlines()
    number_inputs_before_filter=len(text)
    for line in text:
          base=list(line.split('!'))
          if base[0] in base_list:
                     index=base_list.index(base[0])+1
                     if base[1]<base_list[index]:
                         base_list[index-1]=base[0]
                         base_list[index]=base[1]
                         base_list[index+1]=base[2]
          else:
                  base_list+=base
    # print(base_list)

  with open (args.output_filtred, 'w') as f:

                      # print(*base_list, file=f, sep="\n")
                      line = '\n'.join(base_list)
                      f.write(line)
                      #number_x_ray=base_list.count('X-RAY DIFFRACTIO\n')
                      #number_NMR=base_list.count('NM\n')
                      number_inputs_after_filter=int(len(base_list)/3)
  return([number_inputs_before_filter,number_inputs_after_filter])

def main(args):

    global model_name
    if args.input_type == 'pdb_id':

      try:
        struct = PandasPdb().fetch_pdb(args.input)
        model_name = args.input
      except:
        sys.exit()
        
    elif args.input_type == 'structure':

        struct = PandasPdb()
        struct = struct.read_pdb(args.input)
        model_name = re.search('[\d\w]+$', struct.header).group()
        
    global resolution
    try:
          resolution = float(re.search("REMARK\s+2\s+RESOLUTION\.\s+(\d+\.\d+)", struct.pdb_text).group(1))
    except:
          resolution = 100
    
    global header
    try:
         header=re.search("COMPND\s+2\s+MOLECULE\:\s+(.+)\S+", struct.pdb_text).group(1)
    except:
         header=model_name 
    try:
       experiment =re.search("REMARK\s+\d+\s+EXPERIMENT TYPE\s+\:\s+(.+)\S+", struct.pdb_text).group(1)
    except:
       experiment='NMR'
    print(f'{args.input}: {experiment}')
    if  experiment!='NMR':
        permition=filter()
        print(f'entries have been viewd: {permition[0]} entries have been selected: {permition[1]}')

if __name__=='__main__':

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)    
    parser.add_argument('-input', type=str,
#                         help='Path to input file.')
                        help='PDB id or PDB structure in .ent format.')
    parser.add_argument('-input_type', type=str, help='Pass your input type.')
    # parser.add_argument('-halide', type=str, default='F', help='Type of halide')
    parser.add_argument('-output_info', type=str)
    parser.add_argument('-output_filtred', type=str)

    args = parser.parse_args()
    main(args)

