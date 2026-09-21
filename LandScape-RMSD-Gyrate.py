# -*- coding: UTF-8 -*-
import os
# print("protein-protein")
os.system("gmx trjconv -s md_0_1.tpr -f md_0_1_noPBC_MOL.xtc -o md_0_1_noPBC_fit.xtc -fit rot+trans")
# 选择backbone进行计算和输出
os.system("gmx rms -s md_0_1.tpr -f md_0_1_noPBC_fit.xtc -o rmsd-landscape.xvg")
# 同样选择backbone
os.system("gmx gyrate -s md_0_1.tpr -f md_0_1_noPBC_fit.xtc -o gyrate-landscape.xvg")


rmsd = open("rmsd-landscape.xvg","r")
rmsd_lines = [i for i in rmsd]
rmsd.close()

gyrate = open("gyrate-landscape.xvg","r")
gyrate_lines = [i for i in gyrate]
gyrate.close()


head = []
pc1_list = []
pc2_list = []
for i in range(len(rmsd_lines)):
    if rmsd_lines[i][0] == "@":
        head.append(rmsd_lines[i])
    else:
        pc1_list.append(rmsd_lines[i][0:-2])
# print(pc1_list)
for i in range(len(gyrate_lines)):
    if gyrate_lines[i][0] != "@":
        pc2_list.append(gyrate_lines[i][15:22])
# print(pc2_list)
for i in range(len(pc1_list)):
    pc1_list[i] = pc1_list[i] + "    " + pc2_list[i] + "\n"

# print(pc1_list)

pc12 = open("rmsd_gyrate_sham.xvg","w+")
pc12.writelines(head+pc1_list)
pc12.close()


os.system("gmx sham -tsham 310 -nlevels 100 -f rmsd_gyrate_sham.xvg -ls rmsd_gyrate_gibbs.xpm -g rmsd_gyrate.log -lsh enthalpy.xpm -lss entropy.xpm")
#os.system("gmx sham -tsham 300 -nlevels 100 -f pc12_sham.xvg -ls pc12_gibbs.xpm -g pc_12.log -lsh pc12_enthalpy.xpm -lss pc12_entropy.xpm")

# os.system("pip install DuIvyTools  -i https://pypi.tuna.tsinghua.edu.cn/simple")
# os.system("dit xpm_show -f pc12_gibbs.xpm -ip -x RMSD -y Gyrate")
# os.system("dit xpm_show -f pc12_gibbs.xpm -3d -x RMSD -y Gyrate")
os.system("dit xpm_show -f rmsd_gyrate_gibbs.xpm -ip -x RMSD -y Gyrate -o LandScape-2d.tif -ns")
os.system("dit xpm_show -f rmsd_gyrate_gibbs.xpm -3d -x RMSD -y Gyrate -o LandScape-3d.tif -ns")