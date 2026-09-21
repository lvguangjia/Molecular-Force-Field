# -*- coding: UTF-8 -*-
import os
print("protein-protein")
os.system("gmx trjconv -s md_0_1.tpr -f md_0_1_noPBC_MOL.xtc -o md_0_1_noPBC_fit.xtc -fit rot+trans")
print("c-alpha-c-alpha")
os.system("gmx covar -s md_0_1.tpr -f md_0_1_noPBC_fit.xtc -o eigenvalues.xvg -v eigenvectors.trr -xpma covapic.xpm ")
print("c-alpha-c-alpha")
os.system("gmx anaeig -s md_0_1.tpr -f md_0_1_noPBC_fit.xtc -v eigenvectors.trr -first 1 -last 1 -proj pc1.xvg ")
print("c-alpha-c-alpha")
os.system("gmx anaeig -s md_0_1.tpr -f md_0_1_noPBC_fit.xtc -v eigenvectors.trr -first 2 -last 2 -proj pc2.xvg  ")

pc1 = open("pc1.xvg","r")
pc1_lines = [i for i in pc1]
pc1.close()

pc2 = open("pc2.xvg","r")
pc2_lines = [i for i in pc2]
pc2.close()

head = []
pc1_list = []
pc2_list = []
for i in range(len(pc1_lines)):
    if pc1_lines[i][0] == "@":
        head.append(pc1_lines[i])
    else:
        pc1_list.append(pc1_lines[i][0:-2])
# print(pc1_list)
for i in range(len(pc2_lines)):
    if pc2_lines[i][0] != "@":
        pc2_list.append(pc2_lines[i][-10:-1])
# print(pc2_list)
for i in range(len(pc1_list)):
    pc1_list[i] = pc1_list[i] + "  " + pc2_list[i] + "\n"

print(pc1_list)

pc12 = open("pc12_sham.xvg","w+")
pc12.writelines(head+pc1_list)
pc12.close()

os.system("gmx sham -tsham 300 -nlevels 100 -f pc12_sham.xvg -ls pc12_gibbs.xpm -g pc_12.log -lsh pc12_enthalpy.xpm -lss pc12_entropy.xpm")

# os.system("pip install DuIvyTools  -i https://pypi.tuna.tsinghua.edu.cn/simple")
# os.system("dit xpm_show -f pc12_gibbs.xpm -ip")
# os.system("dit xpm_show -f pc12_gibbs.xpm -3d")