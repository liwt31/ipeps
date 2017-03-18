import pyUni10 as uni10
import sys
import numpy as np
#import matplotlib.pyplot as plt
#import matplotlib
#import pylab
import random
import copy
import time
import Move
import MoveCorboz
import MoveFull
import basic_FU
import basicA
import basicB

def Var_H(a_u,b_u,a,b,c,d,Env,D,U,d_phys,chi,Gauge,Positive,Corner_method):
 Truncation=[0]

 c1,c2,c3,c4, Ta1, Ta2, Ta3, Ta4, Tb1, Tb2, Tb3, Tb4=basic_FU.Init_env(Env)

 Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4=rebond_corner(a,b,c,d,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4)

 #t0=time.time()
 if Corner_method is 'CTM':
  c1, c2,c3,c4,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4=corner_transfer_matrix_twosite(a,b,c,d,chi,c1, c2,c3,c4,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4,D)
 if Corner_method is'CTMRG':
  c1, c2,c3,c4,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4=corner_transfer_matrix_twosite_CTMRG(a,b,c,d,chi,c1, c2,c3,c4,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4,D)
 if Corner_method is'CTMFull':
  c1, c2,c3,c4,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4,Truncation=corner_transfer_matrix_twosite_CTMFull(a,b,c,d,chi,c1, c2,c3,c4,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4,D, Truncation)
 #print time.time() - t0, "CTM-H, Left"

 Env=basic_FU.reconstruct_env(c1,c2,c3,c4, Ta1, Ta2, Ta3, Ta4, Tb1, Tb2, Tb3, Tb4,Env)


 #t0=time.time()
 E1, E2, E3, E4, E5,E6=basic_FU.produce_Env_Hab(a,b,c,d,c1, c2,c3,c4,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4,D,d_phys)
 #print time.time() - t0, "Env, Left"

 #basic_FU.test_env(E1, E2, E3, E4, E5,E6, a, b, c1,c2,c3,c4,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4)
 #basic_FU.test_energy(E1, E2, E3, E4, E5,E6, a, b, c1, c2, c3, c4, Ta1, Tb1, Ta2, Tb2, Ta3, Tb3, Ta4, Tb4, a_u, b_u, U)


 N_uni, l, l_d, r, r_d, q_u, qq_u = basic_FU.Qr_lQ_decom(a_u,b_u, E1, E2, E3, E4, E5,E6,D,d_phys)


 #basic_FU.test_energy_lr(N_uni, l, l_d, r, r_d, q_u,qq_u,U,E1, E2, E3, E4, E5,E6,a_u,b_u)

 
 #lp, rp, lp_d, rp_d=basic_FU.initialize_lrprime(l, r, l_d, r_d, N_uni)
 #lp, rp, lp_d, rp_d=basic_FU.initialize_SVD_lrprime(l, r, l_d, r_d, N_uni,U,D,d_phys)
 #t0=time.time() 
 if Gauge is 'Fixed':
  lp, rp, lp_d, rp_d, N_uni, l, r, l_d, r_d,q_u, qq_u, a_u, b_u=basic_FU.initialize_Positiv_lrprime(l, r, l_d, r_d, N_uni, U, D, d_phys, q_u, qq_u,a_u,b_u,Positive)


 #print time.time() - t0, "N, Left"

 #basic_FU.test_energy_lr(N_uni, l, l_d, r, r_d, q_u,qq_u,U,E1, E2, E3, E4, E5,E6,a_u,b_u)
 #basic_FU.test_energy(E1, E2, E3, E4, E5,E6, a, b, c1, c2, c3, c4, Ta1, Tb1, Ta2, Tb2, Ta3, Tb3, Ta4, Tb4, a_u, b_u, U)
 #t0=time.time() 

 rp, rp_d, lp, lp_d=basic_FU.Do_optimization_Full(l, r, l_d, r_d, lp, rp, lp_d, rp_d ,N_uni,U)
 #rp, rp_d, lp, lp_d=basic_FU.Do_optimization_Grad(l, r, l_d, r_d, lp, rp, lp_d, rp_d ,N_uni,U)
 #print time.time() - t0, "Optimization-Full, Left"
 
 
 lp, rp, lp_d, rp_d=basic_FU.Equall_Dist(lp, rp,D,d_phys)
 ap_u, bp_u=basic_FU.recover(lp, rp, q_u, qq_u)
 #Distance_val=basic_FU.Distance(l, r, lp, rp ,N_uni,U)
 #A=basic_FU.final_test_distance(ap_u, bp_u, a_u, b_u,E1, E2, E3, E4, E5,E6,U,N_uni)
 #Distance_val=basic_FU.Distance(l, r, lp, rp ,N_uni,U)
 #print 'Final', A[0], Distance_val[0]
 
 bp_u=max_ten(bp_u)
 ap_u=max_ten(ap_u)
 a=make_ab(ap_u)
 b=make_ab(bp_u)
 return ap_u, bp_u, a, b




def Var_V(c_u,a_u,a,b,c,d,Env,D,U,d_phys,chi,Gauge,Positive,Corner_method):


 c1,c2,c3,c4, Ta1, Ta2, Ta3, Ta4, Tb1, Tb2, Tb3, Tb4=basic_FU.Init_env(Env)

 Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4=rebond_corner(a,b,c,d,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4)



 #t0=time.time()
 if Corner_method is 'CTM':
  c1, c2,c3,c4,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4=corner_transfer_matrix_twosite(a,b,c,d,chi,c1, c2,c3,c4,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4,D)

 if Corner_method is 'CTMRG':
  c1, c2,c3,c4,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4=corner_transfer_matrix_twosite_CTMRG(a,b,c,d,chi,c1, c2,c3,c4,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4,D)

 if Corner_method is 'CTMFull':
  c1, c2,c3,c4,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4=corner_transfer_matrix_twosite_CTMFull(a,b,c,d,chi,c1, c2,c3,c4,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4,D)
 Env=basic_FU.reconstruct_env(c1,c2,c3,c4, Ta1, Ta2, Ta3, Ta4, Tb1, Tb2, Tb3, Tb4,Env)

 #print time.time() - t0, "CTM-V, Left"

 #print 'Truncation', Truncation[0]
 #norm=Move.magnetization_value(c1,c2,c3,c4,Ta1,Ta2,Ta3,Ta4,Tb1,Tb2,Tb3,Tb4,a,b,c,d)
 #print 'norm=', norm[0] 
 
 E1, E2, E3, E4, E5,E6=basic_FU.produce_Env_Hac(a,b,c,d,c1, c2,c3,c4,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4,D,d_phys)

 E1, E2, E3, E4, E5,E6=reorder_env(E1, E2, E3, E4, E5,E6)


 c_u.setLabel([0,1,2,3,4])
 a_u.setLabel([0,1,2,3,4])
 c_u.permute([0,2,3,4,1],3)
 a_u.permute([0,2,3,4,1],3)
 c_u.setLabel([0,1,2,3,4])
 a_u.setLabel([0,1,2,3,4])
 c=make_ab(c_u)
 a=make_ab(a_u)
 
 #basic_FU.test_env(E1, E2, E3, E4, E5,E6, c, a, c1,c2,c3,c4,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4)
 
 #E1, E2, E3, E4, E5,E6=basic_FU.proper_bond(E1, E2, E3, E4, E5,E6,D,d_phys)
 
 #basic_FU.test_energy(E1, E2, E3, E4, E5,E6, c, a, c1, c2, c3, c4, Ta1, Tb1, Ta2, Tb2, Ta3, Tb3, Ta4, Tb4, c_u, a_u, U)
 
 N_uni, l, l_d, r, r_d, q_u, qq_u = basic_FU.Qr_lQ_decom(c_u,a_u, E1, E2, E3, E4, E5,E6,D,d_phys)

 #basic_FU.test_energy_lr(N_uni, l, l_d, r, r_d, q_u,qq_u,U,E1, E2, E3, E4, E5,E6,c_u,a_u)

 #lp, rp, lp_d, rp_d=basic_FU.initialize_lrprime(l, r, l_d, r_d, N_uni)
 #lp, rp, lp_d, rp_d=basic_FU.initialize_SVD_lrprime(l, r, l_d, r_d, N_uni,U,D,d_phys)

 if Gauge is 'Fixed':
  lp, rp, lp_d, rp_d, N_uni, l, r, l_d, r_d,q_u, qq_u, c_u, a_u=basic_FU.initialize_Positiv_lrprime(l, r, l_d, r_d, N_uni, U, D, d_phys, q_u, qq_u,c_u,a_u,Positive)

 #basic_FU.test_energy_lr(N_uni, l, l_d, r, r_d, q_u,qq_u,U,E1, E2, E3, E4, E5,E6,c_u,a_u)


 rp, rp_d, lp, lp_d=basic_FU.Do_optimization_Full(l, r, l_d, r_d, lp, rp, lp_d, rp_d ,N_uni,U)
 #rp, rp_d, lp, lp_d=basic_FU.Do_optimization_Grad(l, r, l_d, r_d, lp, rp, lp_d, rp_d ,N_uni,U)
 
 
 lp, rp, lp_d, rp_d=basic_FU.Equall_Dist(lp, rp,D,d_phys)
 cp_u, ap_u=basic_FU.recover(lp, rp, q_u, qq_u)
 #Distance_val=basic_FU.Distance(l, r, lp, rp ,N_uni,U)
 #A=basic_FU.final_test_distance(cp_u, ap_u, c_u, a_u,E1, E2, E3, E4, E5,E6,U,N_uni)
 #Distance_val=basic_FU.Distance(l, r, lp, rp ,N_uni,U)
 #print 'Final', A[0], Distance_val[0]
 
 cp_u.setLabel([0,1,2,3,4])
 ap_u.setLabel([0,1,2,3,4])

 cp_u.setLabel([0,2,3,4,1])
 ap_u.setLabel([0,2,3,4,1])

 cp_u.permute([0,1,2,3,4],3)
 ap_u.permute([0,1,2,3,4],3)


 cp_u=max_ten(cp_u)
 ap_u=max_ten(ap_u)
 
 cp=make_ab(cp_u)
 ap=make_ab(ap_u)
 
 return cp_u, ap_u, cp, ap


def reorder_env(E1, E2, E3, E4, E5,E6):

 E5p=copy.copy(E1)
 E6p=copy.copy(E2)
 E1p=copy.copy(E3)
 E2p=copy.copy(E4)
 E3p=copy.copy(E5)
 E4p=copy.copy(E6)
 return E1p,E2p,E3p,E4p,E5p,E6p



def Initialize_function(Gamma,Landa):
 q0_even = uni10.Qnum(0,uni10.PRT_EVEN);
 q0_odd = uni10.Qnum(0,uni10.PRT_ODD);
 #Gamma[0].randomize()
 for i in xrange(len(Gamma)):
  Gamma[i].randomize()
  Gamma[i]=Gamma[i]*(1.00/MaxAbs(Gamma[i]))
  
 for i in xrange(len(Landa)):
  #Landa[i].identity()
  blk_qnums = Landa[i].blockQnum()
  for qnum in blk_qnums:
    M=Landa[i].getBlock(qnum)
    if qnum == q0_even:
     #M[0]=1.100
     M.randomize()
     #M.identity()
     #print "M0", M
    else: 
     #M[0]=0.01
     M.randomize()
     #M.identity()

    Landa[i].putBlock(qnum,M)
  Landa[i]=Landa[i]*(1.00/MaxAbs(Landa[i]))

 
def matSx():
  spin = 0.5
  dim = int(spin * 2 + 1)
  return uni10.Matrix(dim, dim, [0.0, 1.0, 1.00, 0.0]);

def matSz():
  spin = 0.5
  dim = int(spin * 2 + 1)
  return uni10.Matrix(dim, dim, [1.0, 0, 0, -1.0]);

def matSy():
  spin = 0.5
  dim = int(spin * 2 + 1)
  return uni10.Matrix(dim, dim, [0.0, -1.00, 1.00, 0.00]);

def transverseIsing_Z2(h,d_phys):
    bdi = uni10.Bond(uni10.BD_IN, d_phys)
    bdo = uni10.Bond(uni10.BD_OUT, d_phys)
    H = uni10.UniTensor([bdi, bdi, bdo, bdo], "Ising")
    H.randomize()
    #print transverseIsing(h).getBlock()
    #H.setRawElem(transverseIsing(h).getBlock().getElem());
    #H.setRawElem(Heisenberg().getBlock());
    blk_qnums=H.blockQnum()
    M=H.getBlock(blk_qnums[0])
    M[0]=-2.0*h*(0.25)
    M[1]=-1.0*(1)
    M[2]=-1.0*(1)
    M[3]=+2.0*h*(0.25)*(1.0)
    H.putBlock(blk_qnums[0],M)

    M=H.getBlock(blk_qnums[1])
    M[0]=-0.0
    M[1]=-1.0*(1)
    M[2]=-1.0*(1)
    M[3]=+0.0
    H.putBlock(blk_qnums[1],M)

    #print H
#    print transverseIsing(h).getBlock().getElem()
    return H



def Heisenberg0_Z2(h,J1,d_phys):
    bdi = uni10.Bond(uni10.BD_IN, d_phys)
    bdo = uni10.Bond(uni10.BD_OUT, d_phys)
    H = uni10.UniTensor([bdi, bdi, bdo, bdo], "Heisenberg")
    #H.randomize()
    #print transverseIsing(h).getBlock()
    #H.setRawElem(transverseIsing(h).getBlock().getElem());
    #H.setRawElem(Heisenberg().getBlock());

    blk_qnums=H.blockQnum()
    M=H.getBlock(blk_qnums[0])
    M[0]=J1*h
    M[1]=0.0
    M[2]=0.0
    M[3]=J1*h
    H.putBlock(blk_qnums[0],M)

    M=H.getBlock(blk_qnums[1])
    M[0]=(-J1)*h
    M[1]=0.5*J1
    M[2]=0.5*J1
    M[3]=(-J1)*h
    H.putBlock(blk_qnums[1],M)

    #print "Symmetric", H
    #print Heisenberg(h).getBlock()
    return H


def Heisenberg1_Z2(J2,d_phys):
    bdi = uni10.Bond(uni10.BD_IN, d_phys)
    bdo = uni10.Bond(uni10.BD_OUT, d_phys)
    H = uni10.UniTensor([bdi, bdi, bdo, bdo], "Heisenberg")
    #H.randomize()
    #print transverseIsing(h).getBlock()
    #H.setRawElem(transverseIsing(h).getBlock().getElem());
    #H.setRawElem(Heisenberg().getBlock());

    blk_qnums=H.blockQnum()
    M=H.getBlock(blk_qnums[0])
    M[0]=J2
    M[1]=0.0
    M[2]=0.0
    M[3]=J2
    H.putBlock(blk_qnums[0],M)

    M=H.getBlock(blk_qnums[1])
    M[0]=(-J2)
    M[1]=2.00*J2
    M[2]=2.00*J2
    M[3]=(-J2)
    H.putBlock(blk_qnums[1],M)

    #print "Symmetric", H
    #print Heisenberg(h).getBlock()
    return H








def Heisenberg0_U1(h,J1, d_phys):
    bdi = uni10.Bond(uni10.BD_IN, d_phys)
    bdo = uni10.Bond(uni10.BD_OUT, d_phys)
    H = uni10.UniTensor([bdi, bdi, bdo, bdo], "Heisenberg")
    #H.randomize()
    #print transverseIsing(h).getBlock()
    #H.setRawElem(transverseIsing(h).getBlock().getElem());
    #H.setRawElem(Heisenberg().getBlock());
    blk_qnums=H.blockQnum()
    blk_qnums[0]
    
    M=H.getBlock(blk_qnums[0])
    M[0]=J1*h
    H.putBlock(blk_qnums[0],M)

    M=H.getBlock(blk_qnums[1])
    M[0]=J1*h
    M[1]=J1*2.0
    M[2]=J1*2.0
    M[3]=J1*h
    H.putBlock(blk_qnums[1],M)


    M=H.getBlock(blk_qnums[2])
    M[0]=J1*h
    H.putBlock(blk_qnums[2],M)


    #print "Symmetric_U1", H
    #print Heisenberg(h).getBlock()
    #H.setRawElem(Heisenberg(h).getBlock().getElem());
    #print "Symmetric", H
    #print Heisenberg(h)

    return H


def Heisenberg1_U1(J2, d_phys):
    bdi = uni10.Bond(uni10.BD_IN, d_phys)
    bdo = uni10.Bond(uni10.BD_OUT, d_phys)
    H = uni10.UniTensor([bdi, bdi, bdo, bdo], "Heisenberg")
    #H.randomize()
    #print transverseIsing(h).getBlock()
    #H.setRawElem(transverseIsing(h).getBlock().getElem());
    #H.setRawElem(Heisenberg().getBlock());
    blk_qnums=H.blockQnum()
    blk_qnums[0]
    M=H.getBlock(blk_qnums[0])
    M[0]=J2
    H.putBlock(blk_qnums[0],M)
    M=H.getBlock(blk_qnums[1])
    M[0]=J2*1.00
    M[1]=J2*2.0
    M[2]=J2*2.0
    M[3]=J2*1.00
    H.putBlock(blk_qnums[1],M)
    M=H.getBlock(blk_qnums[2])
    M[0]=J2
    H.putBlock(blk_qnums[2],M)
    #print "Symmetric_U1", H
    #print Heisenberg(h).getBlock()
    #H.setRawElem(Heisenberg(h).getBlock().getElem());
    #print "Symmetric", H
    #print Heisenberg(h)
    return H





def Heisenberg0(h, J1):
    spin = 0.5
    sx = matSx()
    sy = matSy()
    sz = matSz()
    iden = uni10.Matrix(2,2, [1, 0, 0, 1])
    ham =J1*(h*uni10.otimes(sz,sz)*(1.00/1.00)+(1.00/1.00)*uni10.otimes(sx,sx)+(-1.00/1.00)*uni10.otimes(sy,sy))
    dim = int(spin * 2 + 1)
    bdi = uni10.Bond(uni10.BD_IN, dim);
    bdo = uni10.Bond(uni10.BD_OUT, dim);
    H =  uni10.UniTensor([bdi, bdi, bdo, bdo], "Heisenberg");
    H.putBlock(ham)
    return H

def Heisenberg1(J2):
    spin = 0.5
    sx = matSx()
    sy = matSy()
    sz = matSz()
    iden = uni10.Matrix(2,2, [1, 0, 0, 1])
    ham =J2*(uni10.otimes(sz,sz)*(1.00/1.00)+(1.00/1.00)*uni10.otimes(sx,sx)+(-1.00/1.00)*uni10.otimes(sy,sy))
    dim = int(spin * 2 + 1)
    bdi = uni10.Bond(uni10.BD_IN, dim);
    bdo = uni10.Bond(uni10.BD_OUT, dim);
    H =  uni10.UniTensor([bdi, bdi, bdo, bdo], "Heisenberg");
    H.putBlock(ham)
    return H




def threebody(h,d_phys):
    bdi = uni10.Bond(uni10.BD_IN, d_phys)
    bdo = uni10.Bond(uni10.BD_OUT, d_phys)
    H = uni10.UniTensor([bdi, bdi,bdi, bdo, bdo,bdo], "Heisenberg")

    spin = 0.5
    sx = matSx()
    sy = matSy()
    sz = matSz()
    iden = uni10.Matrix(2,2, [1, 0, 0, 1])
    szt=uni10.otimes(sz,sz)
    sxt=uni10.otimes(sx,sx)
    syt=uni10.otimes(sy,sy)
    ident=uni10.otimes(iden,iden)

    sztt=uni10.otimes(iden,sz)
    sxtt=uni10.otimes(iden,sx)
    sytt=uni10.otimes(iden,sy)

#    ham =(-1.00)*uni10.otimes(szt,iden)+uni10.otimes(sxt,iden)+(-1.0)*uni10.otimes(syt,iden)
#    ham =ham + (-1.00)*uni10.otimes(iden,szt)+uni10.otimes(iden,sxt)+(-1.0)*uni10.otimes(iden,syt)


#    ham =(-1.00)*uni10.otimes(sz,ident)#+uni10.otimes(sxt,iden)+(-1.0)*uni10.otimes(syt,iden)
#    ham =ham + (-1.00)*uni10.otimes(sztt,iden)#+uni10.otimes(iden,sxt)+(-1.0)*uni10.otimes(iden,syt)
#    ham =ham + (-1.00)*uni10.otimes(ident, sz)#+uni10.otimes(iden,sxt)+(-1.0)*uni10.otimes(iden,syt)


    #ham =uni10.otimes(iden,szt)+uni10.otimes(iden,sxt)+(-1.0)*uni10.otimes(iden,syt)
    #ham =uni10.otimes(iden,ident)+uni10.otimes(iden,sxt)+(-1.0)*uni10.otimes(iden,syt)

#    ham =ham + 1.00*(float(h))*(uni10.otimes(sz,sztt)+uni10.otimes(sx,sxtt)+(-1.0)*uni10.otimes(sy,sytt))
    ham = (1.00/1.00)*(float(h))*(uni10.otimes(sz,sztt)+uni10.otimes(sx,sxtt)+(-1.0)*uni10.otimes(sy,sytt))

    H.putBlock(ham)
    #print H
    #H.randomize()
    return H








def threebody_Z2(h,d_phys):
    bdi = uni10.Bond(uni10.BD_IN, d_phys)
    bdo = uni10.Bond(uni10.BD_OUT, d_phys)
    H = uni10.UniTensor([bdi, bdi,bdi, bdo, bdo,bdo], "Heisenberg")
    #H.randomize()
    #H1=copy.copy(H)
    #H1.transpose()
    #H=H+H1
    #print transverseIsing(h).getBlock()
    #H.setRawElem(transverseIsing(h).getBlock().getElem());
    #H.setRawElem(Heisenberg().getBlock());
    blk_qnums=H.blockQnum()
    blk_qnums[0]
    

    M=H.getBlock(blk_qnums[0])
    M[0]=2.0*h+2.00
    M[5]=-2.0*h
    M[10]=2.0*h-2.00
    M[15]=-2.0*h
    M[7]=2.0*2.0*h
    M[13]=2.0*2.0*h
    M[6]=2.00
    M[9]=2.00
    M[11]=2.00
    M[14]=2.00
    
    H.putBlock(blk_qnums[0],M)

    M=H.getBlock(blk_qnums[1])
    M[0]=2.0*h+2.0
    M[5]=-2.0*h
    M[10]=-2.0*h
    M[15]=2.0*h-2.00
    M[6]=2.00*2.0*h
    M[9]=2.00*2.0*h
    M[7]=2.00
    M[11]=2.00
    M[13]=2.00
    M[14]=2.00

    H.putBlock(blk_qnums[1],M)

    #print "Symmetric", H
    #print Heisenberg(h).getBlock()
    return H



def threebody_U1(h,d_phys):
    bdi = uni10.Bond(uni10.BD_IN, d_phys)
    bdo = uni10.Bond(uni10.BD_OUT, d_phys)
    H = uni10.UniTensor([bdi, bdi,bdi, bdo, bdo,bdo], "Heisenberg")
    #H.randomize()
    #H1=copy.copy(H)
    #H1.transpose()
    #H=H+H1
    #print transverseIsing(h).getBlock()
    #H.setRawElem(transverseIsing(h).getBlock().getElem());
    #H.setRawElem(Heisenberg().getBlock());
    blk_qnums=H.blockQnum()
    blk_qnums[0]
    

    M=H.getBlock(blk_qnums[0])
    M[0]=h#+2.00
    H.putBlock(blk_qnums[0],M)

    M=H.getBlock(blk_qnums[1])
    M[0]=-h
    M[1]=0#2
    M[2]=2.0*h
    M[3]=0#2
    M[4]=h#-2
    M[5]=0#2.0
    M[6]=2.0*h
    M[7]=0#2.00
    M[8]=-h
    
    H.putBlock(blk_qnums[1],M)

    M=H.getBlock(blk_qnums[2])
    M[0]=-h
    M[1]=2.0*h
    M[2]=0#2.00
    M[3]=2.0*h
    M[4]=-h
    M[5]=0#2.0
    M[6]=0#2.00
    M[7]=0#2.00
    M[8]=h#-2.00
    
    H.putBlock(blk_qnums[2],M)

    M=H.getBlock(blk_qnums[3])
    M[0]=h#+2.00
    H.putBlock(blk_qnums[3],M)

    #print "Symmetric", H
    #print Heisenberg(h).getBlock()
#    H.setRawElem(threebody(h,d_phys).getBlock().getElem());
#    print "Symmetric", H
    
    
    return H











def makeTab(chi,D):
 bdi = uni10.Bond(uni10.BD_IN, chi)
 bdi1 = uni10.Bond(uni10.BD_IN, D)
 #bdi1.combine(copy.copy(bdi1))
 bdo = uni10.Bond(uni10.BD_OUT, chi)
 Tem0=uni10.UniTensor([bdi, bdi1,bdi1, bdo])
 Tem0.randomize()
 Tem0*=(1.00/MaxAbs(Tem0))
 Tem1=uni10.UniTensor([bdi, bdi1,bdi1, bdo])
 Tem1.randomize()
 Tem1*=(1.00/MaxAbs(Tem1))
 return Tem0, Tem1

def makeTab1(chi,D):
 bdi = uni10.Bond(uni10.BD_IN, chi)
 bdi1 = uni10.Bond(uni10.BD_OUT, D)
 #bdi1.combine(copy.copy(bdi1))
 bdo = uni10.Bond(uni10.BD_OUT, chi)
 Tem0=uni10.UniTensor([bdi, bdi1,bdi1, bdo])
 Tem0.randomize()
 Tem0*=(1.00/Tem0.norm())
 Tem1=uni10.UniTensor([bdi, bdi1,bdi1, bdo])
 Tem1.randomize()
 Tem1*=(1.00/Tem1.norm())
 return Tem0, Tem1

def MaxAbs(c):
 blk_qnums = c.blockQnum()
 max_list=[]
 for qnum in blk_qnums:
    c_mat=c.getBlock(qnum)
    max_list.append(c_mat.absMax())
 #sv_mat = uni10.Matrix( len(max_list), len(max_list), max_list, True)
 #return sv_mat.absMax()
 max_list_f=[abs(x) for x in max_list]
 #print max_list_f, max(max_list_f)
 return max(max_list_f)

 



def makec1(chi,D):
 bdi = uni10.Bond(uni10.BD_IN, chi)
 bdo = uni10.Bond(uni10.BD_OUT, chi)
 
 
 c1=uni10.UniTensor([bdi, bdo])
 c2=uni10.UniTensor([bdi, bdi])
 c3=uni10.UniTensor([bdi, bdo])
 c4=uni10.UniTensor([bdo, bdo])
 c1.randomize()
 c2.randomize()
 c3.randomize()
 c4.randomize()
 c1*=(1.00/MaxAbs(c1))
 c2*=(1.00/MaxAbs(c2))
 c3*=(1.00/MaxAbs(c3))
 c4*=(1.00/MaxAbs(c4))
 return c1,c2,c3,c4
 
def makeab(Landa,Gamma):

 Landa_cp=[ copy.copy(Landa[i]) for i in xrange(len(Landa)) ]

 Landa_sq=sqrt(Landa_cp)

 a_u=copy.copy(Gamma)


 Landa_sq[0].setLabel([-1,1])
 Landa_sq[1].setLabel([-2,2])
 Landa_sq[2].setLabel([3,-3])
 Landa_sq[3].setLabel([4,-4])


 a_u.setLabel([0,1,2,3,4])
 
 a_u=(((((a_u*Landa_sq[0])*Landa_sq[1])*Landa_sq[2])*Landa_sq[3]))
 a_u.permute([0,-1,-2,-3,-4],3)

 a_d=copy.copy(a_u)
 a_d.transpose()
 a_d.setLabel([-3,-4,0,-1,-2])

 a_u.setLabel([0,1,2,3,4])


 a=a_u*a_d
 a.permute([1,-1,2,-2,3,-3,4,-4],4)
# a.combineBond([1,-1])
# a.permute([2,-2,3,-3,4,-4,1],4)
# a.combineBond([2,-2])
# a.permute([3,-3,4,-4,1,2],4)
# a.combineBond([3,-3])
# a.permute([4,-4,1,2,3],4)
# a.combineBond([4,-4])
# a.permute([1,2,3,4],2)

 return a_u, a


 
def   sqrt(Landa):
 Landa_cp=[ copy.copy(Landa[i]) for i in xrange(len(Landa))   ]
 for q in xrange(len(Landa_cp)): 
  blk_qnums=Landa_cp[q].blockQnum()
  for qnum in blk_qnums:
   D=int(Landa_cp[q].getBlock(qnum).col())
   Landa_cpm=Landa_cp[q].getBlock(qnum)
   Landam=Landa[q].getBlock(qnum)
   for i in xrange(D):
    for j in xrange(D):
     Landa_cpm[i*D+j]=Landam[i*D+j]**(1.00/2.00)
   Landa_cp[q].putBlock(qnum,Landa_cpm)
 return Landa_cp

 
def inverse(Landa2):
 invLanda2=uni10.UniTensor(Landa2.bond())
 blk_qnums=Landa2.blockQnum()
 for qnum in blk_qnums:
  D=int(Landa2.getBlock(qnum).row())
  D1=int(Landa2.getBlock(qnum).col())
  invL2 = uni10.Matrix(D, D1)
  invLt = uni10.Matrix(D, D1)
  invLt=Landa2.getBlock(qnum)
  for i in xrange(D):
    for j in xrange(D1):
     invL2[i*D1+j] = 0 if ((invLt[i*D1+j].real) < 1.0e-12) else (1.00 / (invLt[i*D1+j].real))
  invLanda2.putBlock(qnum,invL2)
 return invLanda2
 
 
 








def make_ab(a_u):
 a_u.setLabel([0,1,2,3,4])

 a_uc=copy.copy(a_u)
 a_uc.transpose()
 a_uc.setLabel([-3,-4,0,-1,-2])


 result=a_uc*a_u
 result.permute([1,-1,2,-2,3,-3,4,-4], 4)

 return result




def corner_transfer_matrix_twosite(a,b,c,d,chi,c1, c2,c3,c4,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4,D):
 z1=copy.copy(a)
 z1.identity()
 z2=copy.copy(a)
 z2.randomize()
 z1=z1#+(1.0e-2)*z2
 criteria_val=0
 Accuracy=1.00e-7
 Truncation=[0]
 E0=20.00
 E1=10.00
 Loop_iter=0
 count=0
 #print  '\n', '\n', 'CTM'
 #t0=time.time()
 while Loop_iter is 0:
  count+=1

  #t0=time.time()
  c1, Ta4, Tb4, c4=Move.add_left1(c1,Tb4,Ta4,c4,Tb1,Ta3,a,c,chi,D)
  c1, Ta4, Tb4, c4=Move.add_left1(c1,Tb4,Ta4,c4,Ta1,Tb3,b,d,chi,D)
  #print time.time() - t0, " 2*Left"
  #print c1#,Ta4.printDiagram()

  c2, Ta2, Tb2, c3=Move.add_right1(c2,Ta2,Tb2,c3,Ta1,Tb3,b,d,chi,D)
  c2, Ta2, Tb2, c3=Move.add_right1(c2,Ta2,Tb2,c3,Tb1,Ta3,a,c,chi,D)

  Move.permuteN(a, b,c,d ,c1, c2, c3, c4, Ta1, Tb1, Ta2, Tb2,Ta3, Tb3,Ta4, Tb4)


  c1, Ta1, Tb1, c2=Move.add_left1(c1,Tb1,Ta1,c2,Tb4,Ta2,a,b,chi,D)
  c1, Ta1, Tb1, c2=Move.add_left1(c1,Tb1,Ta1,c2,Ta4,Tb2,c,d,chi,D)

  

  c4, Ta3, Tb3, c3=Move.add_right1(c4,Ta3,Tb3,c3,Ta4,Tb2,c,d,chi,D)
  c4, Ta3, Tb3, c3=Move.add_right1(c4,Ta3,Tb3,c3,Tb4,Ta2,a,b,chi,D)

  Move.permuteN1( a, b, c, d ,c1, c2,c3,c4,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4)

  if (count > 0 )  :
#   print c1.norm(),c2.norm(),c3.norm(),c4.norm()
#   print Ta4.norm(),Ta3.norm(),Ta2.norm(),Ta1.norm()
#   print Tb4.norm(),Tb3.norm(),Tb2.norm(),Tb1.norm()
    
   norm=Move.magnetization_value1(c1,c2,c3,c4,Ta1,Ta2,Ta3,Ta4,Tb1,Tb2,Tb3,Tb4,a,b,c,d)
   norm1=Move.magnetization_value1(c1,c2,c3,c4,Ta1,Ta2,Ta3,Ta4,Tb1,Tb2,Tb3,Tb4,z1,b,c,d)
   #print time.time() - t0, count, "CTM-Norm, Left"

   E0=E1
   if (abs(norm[0]) > 1.00e-10):
    E1=abs(norm1[0])/abs(norm[0])
    if (abs((E0-E1)/E0) < Accuracy) :Loop_iter=1;
   else:
    E1=abs(norm1[0])
    if (abs((E0-E1)) < Accuracy) : print 'Warning: norm~0', E1; Loop_iter=1;
   if (count > 10 ): print 'break! CTM'; break;
   print E1, abs((E0-E1)/E1),norm[0],  count
   #print E1, Truncation[0], abs((E0-E1)/E1)
   #print a.norm(), b.norm(), c.norm(), d.norm()
 
 #print 'CTM', norm[0], count, c2
 #c2.permute([0,1],1)
 #print c2
 #print time.time() - t0, count, "CTM, Left"



 return c1, c2,c3,c4,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4



def corner_transfer_matrix_twosite_CTMRG(a,b,c,d,chi,c1, c2,c3,c4,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4,D):
 z1=copy.copy(a)
 z1.identity()
 z2=copy.copy(a)
 z2.randomize()
 z1=z1#+(1.0e-2)*z2
 Accuracy=1.00e-7
 E0=20.00
 E1=10.00
 Loop_iter=0
 count=0
 #print  '\n', '\n', 'CTM'
# norm=Move.magnetization_value1(c1,c2,c3,c4,Ta1,Ta2,Ta3,Ta4,Tb1,Tb2,Tb3,Tb4,a,b,c,d)
# print "f",norm[0]
 
 while Loop_iter is 0: 

  c1, Ta4, Tb4, c4, c2, Ta2, Tb2, c3=MoveCorboz.add_left1(c1,c2,c3,c4,Ta1,Ta2,Ta3,Ta4,Tb1,Tb2,Tb3,Tb4,a,b,c,d,chi,D)
#  norm=Move.magnetization_value1(c1,c2,c3,c4,Ta1,Ta2,Ta3,Ta4,Tb1,Tb2,Tb3,Tb4,a,b,c,d)
#  print "f",norm[0]
  
  #print c1.printDiagram(),c2.printDiagram(), c4.printDiagram(),c3.printDiagram()
  #print Ta4.printDiagram(),Tb4.printDiagram(),Ta2.printDiagram(),Tb2.printDiagram()
  c1, Ta4, Tb4, c4, c2, Ta2, Tb2, c3=MoveCorboz.add_left1(c1,c2,c3,c4,Tb1,Ta2,Tb3,Ta4,Ta1,Tb2,Ta3,Tb4,b,a,d,c,chi,D) 
  #print c1.printDiagram()#
#  norm=Move.magnetization_value1(c1,c2,c3,c4,Ta1,Ta2,Ta3,Ta4,Tb1,Tb2,Tb3,Tb4,a,b,c,d)
#  print "f",norm[0]

  MoveCorboz.permuteN(a, b,c,d ,c1, c2,c3,c4,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4)

#  print c1.norm(), c2.norm(), c3.norm(), c4.norm()
  c1, Ta1, Tb1, c2, c4, Ta3, Tb3, c3=MoveCorboz.add_left1(c1,c4,c3,c2,Ta4,Ta3,Ta2,Ta1,Tb4,Tb3,Tb2,Tb1,a,c,b,d,chi,D)
  
#  print c1.norm(), c2.norm(), c3.norm(), c4.norm()
#  print Ta4.norm(), Ta3.norm(), Ta2.norm(), Ta1.norm()
#  print Tb4.norm(), Tb3.norm(), Tb2.norm(), Tb1.norm()

  c1, Ta1, Tb1, c2, c4, Ta3, Tb3, c3=MoveCorboz.add_left1(c1,c4,c3,c2,Tb4,Ta3,Tb2,Ta1,Ta4,Tb3,Ta2,Tb1,c,a,d,b,chi,D)

  MoveCorboz.permuteN1(a, b,c,d ,c1, c2,c3,c4,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4)

#  print c1.norm(), c2.norm(), c3.norm(), c4.norm()
#  print Ta4.norm(), Ta3.norm(), Ta2.norm(), Ta1.norm()
#  print Tb4.norm(), Tb3.norm(), Tb2.norm(), Tb1.norm()

#  c1,c2,c3,c4,Ta1,Tb1,Ta2,Tb2,Ta3,Tb3,Ta4,Tb4=Move.test_env_Ten(c1,c2,c3,c4,Ta1,Tb1,Ta2,Tb2,Ta3,Tb3,Ta4,Tb4)
#  criteria_val=Move.distance(c1, c2, c3, c4, c1_f, c2_f, c3_f, c4_f)

  
  norm=MoveCorboz.magnetization_value(c1,c2,c3,c4,Ta1,Ta2,Ta3,Ta4,Tb1,Tb2,Tb3,Tb4,a,b,c,d)
  norm1=MoveCorboz.magnetization_value(c1,c2,c3,c4,Ta1,Ta2,Ta3,Ta4,Tb1,Tb2,Tb3,Tb4,z1,b,c,d)
  E0=E1
  if (abs(norm[0]) > 1.00e-10):
   E1=abs(norm1[0])/abs(norm[0])
   if (abs((E0-E1)/E0) < Accuracy):Loop_iter=1;
  else:
   E1=abs(norm1[0])
   if (abs((E0-E1)) < Accuracy) : print 'Warning: norm~0', E1; Loop_iter=1;
  count+=1
  if (count > 15 ): print 'break! CTM'; break;
  #print E1, abs((E0-E1)/E1),norm[0], count
  #print E1, Truncation[0], abs((E0-E1)/E1)
  #print a.norm(), b.norm(), c.norm(), d.norm()
 
 #print 'CTM', norm[0]
 return c1, c2,c3,c4,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4


def corner_transfer_matrix_twosite_CTMFull(ap,bp,cp,dp,chi,c1, c2,c3,c4,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4,D):
 a=copy.copy(ap)
 b=copy.copy(bp)
 c=copy.copy(cp)
 d=copy.copy(dp)

 a.setLabel([1,-1,2,-2,3,-3,4,-4])
 b.setLabel([1,-1,2,-2,3,-3,4,-4])
 c.setLabel([1,-1,2,-2,3,-3,4,-4])
 d.setLabel([1,-1,2,-2,3,-3,4,-4])



 a.combineBond([1,-1])
 a.combineBond([2,-2])
 a.combineBond([3,-3])
 a.combineBond([4,-4])
 b.combineBond([1,-1])
 b.combineBond([2,-2])
 b.combineBond([3,-3])
 b.combineBond([4,-4])
 c.combineBond([1,-1])
 c.combineBond([2,-2])
 c.combineBond([3,-3])
 c.combineBond([4,-4])
 d.combineBond([1,-1])
 d.combineBond([2,-2])
 d.combineBond([3,-3])
 d.combineBond([4,-4])
 Ta11=copy.copy(Ta1)
 Ta22=copy.copy(Ta2)
 Ta33=copy.copy(Ta3)
 Ta44=copy.copy(Ta4)
 
 Tb11=copy.copy(Tb1)
 Tb22=copy.copy(Tb2)
 Tb33=copy.copy(Tb3)
 Tb44=copy.copy(Tb4)
 c3.transpose()
 
 
 Ta1.setLabel([1,2,-2,3])
 Ta1.combineBond([2,-2])
 Ta2.setLabel([1,2,-2,3])
 Ta2.combineBond([2,-2])
 Ta3.setLabel([1,2,-2,3])
 Ta3.combineBond([2,-2])
 Ta4.setLabel([1,2,-2,3])
 Ta4.combineBond([2,-2])
 Tb4.setLabel([1,2,-2,3])
 Tb4.combineBond([2,-2])
 Tb3.setLabel([1,2,-2,3])
 Tb3.combineBond([2,-2])
 Tb2.setLabel([1,2,-2,3])
 Tb2.combineBond([2,-2])
 Tb1.setLabel([1,2,-2,3])
 Tb1.combineBond([2,-2])



 chi=20
 z1=copy.copy(a)
 z2=copy.copy(b)
 z2.randomize()
 z1.identity()
 z1=z1#+(1.00e-5)*z2
 Accuracy=1.00e-7
 Truncation=[0]
 E0=20.00
 E1=10.00
 Loop_iter=0
 count=0
 #print  '\n', '\n', 'CTM'
 while Loop_iter is 0: 
  c1_f=copy.copy(c1)
  c2_f=copy.copy(c2)
  c3_f=copy.copy(c3)
  c4_f=copy.copy(c4)

  c1, Ta4, Tb4, c4, c2, Ta2, Tb2, c3=MoveFull.add_left(c1,c2,c3,c4,Ta1,Ta2,Ta3,Ta4,Tb1,Tb2,Tb3,Tb4,a,b,c,d,chi,D)
  
  c1, Ta4, Tb4, c4, c2, Ta2, Tb2, c3=MoveFull.add_left (c1,c2,c3,c4,Tb1,Ta2,Tb3,Ta4,Ta1,Tb2,Ta3,Tb4,b,a,d,c,chi,D)
  MoveFull.permute(a, b,c,d ,c1, c2,c3,c4,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4)

  c1, Ta1, Tb1, c2, c4, Ta3, Tb3, c3=MoveFull.add_left(c1,c4,c3,c2,Ta4,Ta3,Ta2,Ta1,Tb4,Tb3,Tb2,Tb1,a,c,b,d,chi,D)
  
  
  c1, Ta1, Tb1, c2, c4, Ta3, Tb3, c3=MoveFull.add_left (c1,c4,c3,c2,Tb4,Ta3,Tb2,Ta1,Ta4,Tb3,Ta2,Tb1,c,a,d,b,chi,D)

  MoveFull.permute(a, b,c,d ,c1, c2,c3,c4,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4)

#  c1,c2,c3,c4,Ta1,Tb1,Ta2,Tb2,Ta3,Tb3,Ta4,Tb4=Move.test_env_Ten(c1,c2,c3,c4,Ta1,Tb1,Ta2,Tb2,Ta3,Tb3,Ta4,Tb4)
  
#  criteria_val=Move.distance(c1, c2, c3, c4, c1_f, c2_f, c3_f, c4_f)
  
  norm=MoveFull.magnetization_value(c1,c2,c3,c4,Ta1,Ta2,Ta3,Ta4,Tb1,Tb2,Tb3,Tb4,a,b,c,d)
  norm1=MoveFull.magnetization_value(c1,c2,c3,c4,Ta1,Ta2,Ta3,Ta4,Tb1,Tb2,Tb3,Tb4,z1,b,c,d)
  E0=E1
  if (abs(norm[0]) > 1.00e-10):
   E1=abs(norm1[0])/abs(norm[0])
   if (abs((E0-E1)/E0) < Accuracy):Loop_iter=1;
  else:
   E1=abs(norm1[0])
   if (abs((E0-E1)) < Accuracy) : print 'Warning: norm~0', E1; Loop_iter=1;
  count+=1
  if (count > 10 ): print 'break! CTM'; break;
  print E1, abs((E0-E1)/E1), norm[0], count
  #print E1, Truncation[0], abs((E0-E1)/E1)
  #print a.norm(), b.norm(), c.norm(), d.norm()
 
 print 'CTM', norm[0]
 c3.transpose()
 

 M=Ta1.getBlock()
 Ta11.putBlock(M)
 
 M=Ta2.getBlock()
 Ta22.putBlock(M)
 Ta3.permute([10,12,13],1)
 M=Ta3.getBlock()
 Ta33.putBlock(M)

 Ta4.permute([11,17,18],1)

 M=Ta4.getBlock()
 Ta44.putBlock(M)

 M=Tb1.getBlock()
 Tb11.putBlock(M)
 M=Tb2.getBlock()
 Tb22.putBlock(M)

 Tb3.permute([13,14,8],1)


 M=Tb3.getBlock()
 Tb33.putBlock(M)

 #print Tb4.printDiagram(),Tb44.printDiagram() 

 Tb4.permute([18,3,0],1)
 M=Tb4.getBlock()
 Tb44.putBlock(M)

 
 return c1, c2,c3,c4,Ta11, Tb11,Ta22, Tb22,Ta33, Tb33,Ta44, Tb44





def E_total(a_u,b_u,c_u,d_u,a,b,c,d,Env,Env1,Env2,Env3,D,h,d_phys,chi,Corner_method,Model):
# print "Total"
#########################
# E_val1=Energy_cab(a_u,b_u,c_u,a,b,c,d,Env,D,h,d_phys,chi,Corner_method,Model)
# print "E_val1", E_val1

# E_val2=Energy_acd(a_u,b_u,d_u,a,b,c,d,Env,D,h,d_phys,chi,Corner_method,Model)
# print "E_val2", E_val2
#########################
# E_val3=Energy_cab(b_u,a_u,d_u,b,a,d,c,Env1,D,h,d_phys,chi,Corner_method,Model)
# print "E_val3", E_val3

# E_val4=Energy_acd(b_u,a_u,c_u,b,a,d,c,Env1,D,h,d_phys,chi,Corner_method,Model)
# print "E_val4", E_val4
#########################
# E_val5=Energy_cab(c_u,d_u,a_u,c,d,a,b,Env2,D,h,d_phys,chi,Corner_method,Model)
# print "E_val5", E_val5

# E_val6=Energy_acd(c_u,d_u,b_u,c,d,a,b,Env2,D,h,d_phys,chi,Corner_method,Model)
# print "E_val6", E_val6
##########################
# E_val7=Energy_cab(d_u,c_u,b_u,d,c,b,a,Env3,D,h,d_phys,chi,Corner_method,Model)
# print "E_val7", E_val7

# E_val8=Energy_acd(d_u,c_u,a_u,d,c,b,a,Env3,D,h,d_phys,chi,Corner_method,Model)
# print "E_val8", E_val8
#########################
# print E_val1,E_val2,E_val3, E_val4, (E_val1+E_val2+E_val3+E_val4) / 4.00
# print E_val5,E_val6,E_val7, E_val8, (E_val5+E_val6+E_val7+E_val8) / 4.00

########################

 E_ab=Energy_h(a_u,b_u,a,b,c,d,Env,D,h,d_phys,chi,Corner_method,Model)
 print E_ab 
 E_ca=Energy_v(c_u,a_u,a,b,c,d,Env,D,h,d_phys,chi,Corner_method,Model)
 print E_ca
 E_cd=Energy_h(c_u,d_u,c,d,a,b,Env1,D,h,d_phys,chi,Corner_method,Model)
 print E_cd
 E_ac=Energy_v(a_u,c_u,c,d,a,b,Env1,D,h,d_phys,chi,Corner_method,Model)
 print E_ac 
 E_ba=Energy_h(b_u,a_u,b,a,d,c,Env2,D,h,d_phys,chi,Corner_method,Model)
 print E_ba
 E_db=Energy_v(d_u,b_u,b,a,d,c,Env2,D,h,d_phys,chi,Corner_method,Model)
 print E_db
 E_dc=Energy_h(d_u,c_u,d,c,b,a,Env3,D,h,d_phys,chi,Corner_method,Model)
 print E_dc
 E_bd=Energy_v(b_u,d_u,d,c,b,a,Env3,D,h,d_phys,chi,Corner_method,Model)
 print E_bd

 print E_ab,E_ba,E_cd, E_dc, (E_ab+E_ba+E_cd+E_dc) / 4.00  
 print E_ca,E_ac,E_db, E_bd, (E_ca+E_ac+E_db+E_bd) / 4.00


 return ((E_ca+E_ac+E_db+E_bd) / 4.00) + ((E_ab+E_ba+E_cd+E_dc) / 4.00)#+((E_val1+E_val2+E_val3+E_val4) / 4.00) + ((E_val5+E_val6+E_val7+E_val8) / 4.00)


def E_total_conv(a_u,b_u,c_u,d_u,a,b,c,d,Env,Env1,Env2,Env3,D,h,d_phys,chi,Corner_method,Model):

# E_val1=Energy_cab(a_u,b_u,c_u,a,b,c,d,Env,D,h,d_phys,chi,Corner_method,Model)
# print "E_val1", E_val1

# E_val2=Energy_acd(a_u,b_u,d_u,a,b,c,d,Env,D,h,d_phys,chi,Corner_method,Model)
# print "E_val2", E_val2
#########################
# E_val3=Energy_cab(b_u,a_u,d_u,b,a,d,c,Env1,D,h,d_phys,chi,Corner_method,Model)
# print "E_val3", E_val3

# E_val4=Energy_acd(b_u,a_u,c_u,b,a,d,c,Env1,D,h,d_phys,chi,Corner_method,Model)
# print "E_val4", E_val4
#########################
# E_val5=Energy_cab(c_u,d_u,a_u,c,d,a,b,Env2,D,h,d_phys,chi,Corner_method,Model)
# print "E_val5", E_val5

# E_val6=Energy_acd(c_u,d_u,b_u,c,d,a,b,Env2,D,h,d_phys,chi,Corner_method,Model)
# print "E_val6", E_val6
##########################
# E_val7=Energy_cab(d_u,c_u,b_u,d,c,b,a,Env3,D,h,d_phys,chi,Corner_method,Model)
# print "E_val7", E_val7

# E_val8=Energy_acd(d_u,c_u,a_u,d,c,b,a,Env3,D,h,d_phys,chi,Corner_method,Model)
# print "E_val8", E_val8
#########################
# print E_val1,E_val2,E_val3, E_val4, (E_val1+E_val2+E_val3+E_val4) / 4.00
# print E_val5,E_val6,E_val7, E_val8, (E_val5+E_val6+E_val7+E_val8) / 4.00

########################

 E_ab=Energy_h(a_u,b_u,a,b,c,d,Env,D,h,d_phys,chi,Corner_method,Model)
 E_ca=Energy_v(c_u,a_u,a,b,c,d,Env,D,h,d_phys,chi,Corner_method,Model)

 E_cd=Energy_h(c_u,d_u,c,d,a,b,Env1,D,h,d_phys,chi,Corner_method,Model)
 E_ac=Energy_v(a_u,c_u,c,d,a,b,Env1,D,h,d_phys,chi,Corner_method,Model)
 
 E_ba=Energy_h(b_u,a_u,b,a,d,c,Env2,D,h,d_phys,chi,Corner_method,Model)
 E_db=Energy_v(d_u,b_u,b,a,d,c,Env2,D,h,d_phys,chi,Corner_method,Model)

 E_dc=Energy_h(d_u,c_u,d,c,b,a,Env3,D,h,d_phys,chi,Corner_method,Model)
 E_bd=Energy_v(b_u,d_u,d,c,b,a,Env3,D,h,d_phys,chi,Corner_method,Model)


 #print E_ab,E_ba,E_cd, E_dc, (E_ab+E_ba+E_cd+E_dc) / 4.00  
 #print E_ca,E_ac,E_db, E_bd, (E_ca+E_ac+E_db+E_bd) / 4.00


 return ((E_ca+E_ac+E_db+E_bd) / 4.00) + ((E_ab+E_ba+E_cd+E_dc) / 4.00)#+((E_val1+E_val2+E_val3+E_val4) / 4.00) + ((E_val5+E_val6+E_val7+E_val8) / 4.00)


def Energy_v(c_u,a_u,a,b,c,d,Env,D,h,d_phys,chi,Corner_method,Model):
 Truncation=[0]
 

 c1,c2,c3,c4, Ta1, Ta2, Ta3, Ta4, Tb1, Tb2, Tb3, Tb4=basic_FU.Init_env(Env)
 
 Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4=rebond_corner(a,b,c,d,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4)


 if Corner_method is 'CTM':
  c1, c2,c3,c4,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4=corner_transfer_matrix_twosite(a,b,c,d,chi,c1, c2,c3,c4,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4,D)
 if Corner_method is 'CTMRG':
  c1, c2,c3,c4,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4=corner_transfer_matrix_twosite_CTMRG(a,b,c,d,chi,c1, c2,c3,c4,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4,D)
 if Corner_method is 'CTMFull':
  c1, c2,c3,c4,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4=corner_transfer_matrix_twosite_CTMFull(a,b,c,d,chi,c1, c2,c3,c4,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4,D)

 

 basic_FU.reconstruct_env(c1,c2,c3,c4, Ta1, Ta2, Ta3, Ta4, Tb1, Tb2, Tb3, Tb4,Env)

 E1, E2, E3, E4, E5,E6=produce_Env_Hac(a,b,c,d,c1, c2,c3,c4,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4,D,d_phys)

 E1, E2, E3, E4, E5,E6=reorder_env(E1, E2, E3, E4, E5,E6)
 cp_u=copy.copy(c_u)
 ap_u=copy.copy(a_u)
 cp=copy.copy(c)
 ap=copy.copy(a)
 
 cp_u.setLabel([0,1,2,3,4])
 ap_u.setLabel([0,1,2,3,4])

 cp_u.permute([0,2,3,4,1],3)
 ap_u.permute([0,2,3,4,1],3)
 cp_u.setLabel([0,1,2,3,4])
 ap_u.setLabel([0,1,2,3,4])
 cp=make_ab(cp_u)
 ap=make_ab(ap_u)
 
 #test_env(E1, E2, E3, E4, E5,E6, cp, ap, c1,c2,c3,c4,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4)
 
 #E1, E2, E3, E4, E5,E6=proper_bond(E1, E2, E3, E4, E5,E6,D,d_phys,c_u,a_u)
 if Model is "Heisenberg":
   H0=Heisenberg0(h[0],h[1])
   H1=Heisenberg1(h[2])
 if Model is "Heisenberg_Z2":
   H0=Heisenberg0_Z2(h[0],h[1],d_phys)
   H1=Heisenberg1_Z2(h[2],d_phys)
 if Model is "Heisenberg_U1":
   H0=Heisenberg0_U1(h[0],h[1],d_phys)
   H1=Heisenberg1_U1(h[2],d_phys)

 E_ca=test_energy(E1, E2, E3, E4, E5,E6, cp, ap, c1, c2, c3, c4, Ta1, Tb1, Ta2, Tb2, Ta3, Tb3, Ta4, Tb4, cp_u, ap_u, H0)
 
 return E_ca


def rebond_corner(a,b,c,d,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4):

 bd=uni10.Bond(uni10.BD_OUT,a.bond(0).Qlist())
 bd1=uni10.Bond(uni10.BD_OUT,a.bond(1).Qlist())

 tempo=copy.copy(Tb4)
 bd_list=[Tb4.bond(0),bd,bd1,Tb4.bond(3)]
 Tb4.assign(bd_list)
 blk_qnums = Tb4.blockQnum()
 blk_qnums1 = tempo.blockQnum()

 for qnum in blk_qnums:
  mat_t=Tb4.getBlock(qnum)
  dx=int(mat_t.row())
  dy=int(mat_t.col())
  if qnum in blk_qnums1: 
   sv_mat=tempo.getBlock(qnum)
  else:
   print "changing Tb4 dimension"      
   sv_mat=uni10.Matrix(dx,dy)
   sv_mat.randomize()
  Tb4.putBlock(qnum,sv_mat.resize(dx,dy) )
 
 #print "Tb4",tempo.printDiagram(),Tb4.printDiagram(),a.printDiagram()
 #print "Tb4", tempo[10],Tb4[10],tempo.elemCmp(Tb4)#,Tb4.printDiagram(),
################################################################

 bd=uni10.Bond(uni10.BD_OUT,c.bond(0).Qlist())
 bd1=uni10.Bond(uni10.BD_OUT,c.bond(1).Qlist())
 
 tempo=copy.copy(Ta4)
 bd_list=[Ta4.bond(0),bd,bd1,Ta4.bond(3)]
 Ta4.assign(bd_list)
 blk_qnums = Ta4.blockQnum()
 blk_qnums1 = tempo.blockQnum()

 for qnum in blk_qnums:
  mat_t=Ta4.getBlock(qnum)
  dx=int(mat_t.row())
  dy=int(mat_t.col())
  if qnum in blk_qnums1: 
   sv_mat=tempo.getBlock(qnum)
  else:
   print "changing Ta4 dimension"      
   sv_mat=uni10.Matrix(dx,dy)
   sv_mat.randomize()
  Ta4.putBlock(qnum,sv_mat.resize(dx,dy) )
 #print "Ta4", Ta4.printDiagram(),Ta4[4]
 #print "Ta4", tempo.elemCmp(Ta4),Tb4.printDiagram(),

##################################################################

 bd=uni10.Bond(uni10.BD_IN,b.bond(4).Qlist())
 bd1=uni10.Bond(uni10.BD_IN,b.bond(5).Qlist())

 tempo=copy.copy(Ta2)
 bd_list=[Ta2.bond(0),bd,bd1,Ta2.bond(3)]
 Ta2.assign(bd_list)
 blk_qnums = Ta2.blockQnum()
 blk_qnums1 = tempo.blockQnum()

 for qnum in blk_qnums:
  mat_t=Ta2.getBlock(qnum)
  dx=int(mat_t.row())
  dy=int(mat_t.col())
  if qnum in blk_qnums1: 
   sv_mat=tempo.getBlock(qnum)
  else:
   print "changing Ta2 dimension"      
   sv_mat=uni10.Matrix(dx,dy)
   sv_mat.randomize()
  Ta2.putBlock(qnum,sv_mat.resize(dx,dy) )
# print "Ta2", Ta2.printDiagram(),Ta2[3]
# print "Ta2", tempo.elemCmp(Ta2),Tb4.printDiagram(),



 bd=uni10.Bond(uni10.BD_IN,d.bond(4).Qlist())
 bd1=uni10.Bond(uni10.BD_IN,d.bond(5).Qlist())


 tempo=copy.copy(Tb2)
 bd_list=[Tb2.bond(0),bd,bd1,Tb2.bond(3)]
 Tb2.assign(bd_list)
 blk_qnums = Tb2.blockQnum()
 blk_qnums1 = tempo.blockQnum()

 for qnum in blk_qnums:
  mat_t=Tb2.getBlock(qnum)
  dx=int(mat_t.row())
  dy=int(mat_t.col())
  if qnum in blk_qnums1: 
   sv_mat=tempo.getBlock(qnum)
  else:
   print "changing Tb2 dimension"    
   sv_mat=uni10.Matrix(dx,dy)
   sv_mat.randomize()
  Tb2.putBlock(qnum,sv_mat.resize(dx,dy) )
# print "Tb2", Tb2.printDiagram(),Tb2[4]
# print "Tb2", tempo.elemCmp(Tb2),Tb4.printDiagram(),

################################################################3
 bd=uni10.Bond(uni10.BD_IN,a.bond(6).Qlist())
 bd1=uni10.Bond(uni10.BD_IN,a.bond(7).Qlist())

 tempo=copy.copy(Tb1)
 bd_list=[Tb1.bond(0),bd,bd1,Tb1.bond(3)]
 Tb1.assign(bd_list)
 blk_qnums = Tb1.blockQnum()
 blk_qnums1 = tempo.blockQnum()

 for qnum in blk_qnums:
  mat_t=Tb1.getBlock(qnum)
  dx=int(mat_t.row())
  dy=int(mat_t.col())
  if qnum in blk_qnums1: 
   sv_mat=tempo.getBlock(qnum)
  else:
   print "changing Tb1 dimension"  
   sv_mat=uni10.Matrix(dx,dy)
   sv_mat.randomize()
  Tb1.putBlock(qnum,sv_mat.resize(dx,dy) )
# print "Tb1", Tb1.printDiagram(),Tb1[4]
# print "Tb1", tempo.elemCmp(Tb1),Tb4.printDiagram(),


 bd=uni10.Bond(uni10.BD_IN,b.bond(6).Qlist())
 bd1=uni10.Bond(uni10.BD_IN,b.bond(7).Qlist())

 tempo=copy.copy(Ta1)
 bd_list=[Ta1.bond(0),bd,bd1,Ta1.bond(3)]
 Ta1.assign(bd_list)
 blk_qnums = Ta1.blockQnum()
 blk_qnums1 = tempo.blockQnum()

 for qnum in blk_qnums:
  mat_t=Ta1.getBlock(qnum)
  dx=int(mat_t.row())
  dy=int(mat_t.col())
  if qnum in blk_qnums1: 
   sv_mat=tempo.getBlock(qnum)
  else:
   print "changing Ta1 dimension"  
   sv_mat=uni10.Matrix(dx,dy)
   sv_mat.randomize()
  Ta1.putBlock(qnum,sv_mat.resize(dx,dy) )
 #print "Ta1",tempo.printDiagram(),Ta1.printDiagram(),b.printDiagram()
 #print "Ta1", tempo[10],Ta1[10],tempo.elemCmp(Ta1)#,Tb4.printDiagram(),

######################################################
 bd=uni10.Bond(uni10.BD_OUT,c.bond(2).Qlist())
 bd1=uni10.Bond(uni10.BD_OUT,c.bond(3).Qlist())

 tempo=copy.copy(Ta3)
 bd_list=[Ta3.bond(0),bd,bd1,Ta3.bond(3)]
 Ta3.assign(bd_list)
 blk_qnums = Ta3.blockQnum()
 blk_qnums1 = tempo.blockQnum()

 for qnum in blk_qnums:
  mat_t=Ta3.getBlock(qnum)
  dx=int(mat_t.row())
  dy=int(mat_t.col())
  if qnum in blk_qnums1: 
   sv_mat=tempo.getBlock(qnum)
  else:
   print "changing Ta3 dimension"  
   sv_mat=uni10.Matrix(dx,dy)
   sv_mat.randomize()
  Ta3.putBlock(qnum,sv_mat.resize(dx,dy) )
 #print "Ta3", Ta3.printDiagram(),Ta3[4]
 #print "Ta3", tempo.elemCmp(Ta3),Tb4.printDiagram(),
 
 
 
 bd=uni10.Bond(uni10.BD_OUT,d.bond(2).Qlist())
 bd1=uni10.Bond(uni10.BD_OUT,d.bond(3).Qlist())

 tempo=copy.copy(Tb3)
 bd_list=[Tb3.bond(0),bd,bd1,Tb3.bond(3)]
 Tb3.assign(bd_list)
 blk_qnums = Tb3.blockQnum()
 blk_qnums1 = tempo.blockQnum()

 for qnum in blk_qnums:
  mat_t=Tb3.getBlock(qnum)
  dx=int(mat_t.row())
  dy=int(mat_t.col())
  if qnum in blk_qnums1: 
   sv_mat=tempo.getBlock(qnum)
  else:
   print "changing Tb3 dimension"
   sv_mat=uni10.Matrix(dx,dy)
   sv_mat.randomize()
  Tb3.putBlock(qnum,sv_mat.resize(dx,dy) )
 #print "Tb3", Tb3.printDiagram(),Tb3[4]
 #print "Tb3", tempo.elemCmp(Tb3),Tb4.printDiagram(),

################################################ 

 return Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4


def Energy_h(a_u,b_u,a,b,c,d,Env,D,h,d_phys,chi,Corner_method,Model):

 c1,c2,c3,c4, Ta1, Ta2, Ta3, Ta4, Tb1, Tb2, Tb3, Tb4=basic_FU.Init_env(Env)

 
 Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4=rebond_corner(a,b,c,d,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4)

# Ta1.randomize(),Tb1.randomize()
# Ta2.randomize(),Tb2.randomize()
# Ta3.randomize(),Tb3.randomize()
# Ta4.randomize(),Tb4.randomize()


 if Corner_method is 'CTM':
  c1, c2,c3,c4,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4=corner_transfer_matrix_twosite(a,b,c,d,chi,c1, c2,c3,c4,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4,D)
 if Corner_method is 'CTMRG':
  c1, c2,c3,c4,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4=corner_transfer_matrix_twosite_CTMRG(a,b,c,d,chi,c1, c2,c3,c4,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4,D)
 if Corner_method is 'CTMFull':
  c1, c2,c3,c4,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4=corner_transfer_matrix_twosite_CTMFull(a,b,c,d,chi,c1, c2,c3,c4,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4,D)


 basic_FU.reconstruct_env(c1,c2,c3,c4, Ta1, Ta2, Ta3, Ta4, Tb1, Tb2, Tb3, Tb4,Env)

 E1, E2, E3, E4, E5,E6=produce_Env_Hab(a,b,c,d,c1, c2,c3,c4,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4,D,d_phys)
 
 
 #test_env(E1, E2, E3, E4, E5,E6, a, b, c1,c2,c3,c4,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4)

 #E1, E2, E3, E4, E5,E6=proper_bond(E1, E2, E3, E4, E5,E6,D,d_phys,a_u,b_u)
 
 if Model is "Heisenberg":
   H0=Heisenberg0(h[0],h[1])
   H1=Heisenberg1(h[2])
 if Model is "Heisenberg_Z2":
   H0=Heisenberg0_Z2(h[0],h[1],d_phys)
   H1=Heisenberg1_Z2(h[2],d_phys)
 if Model is "Heisenberg_U1":
   H0=Heisenberg0_U1(h[0],h[1],d_phys)
   H1=Heisenberg1_U1(h[2],d_phys)
   
   
 E_ab=test_energy(E1, E2, E3, E4, E5,E6, a, b, c1, c2, c3, c4, Ta1, Tb1, Ta2, Tb2, Ta3, Tb3, Ta4, Tb4, a_u, b_u, H0)
 
########################################################################3 
 return E_ab




def Energy_cab(a_u,b_u,c_u,a,b,c,d,Env,D,h,d_phys,chi,Corner_method,Model):


 
 c1,c2,c3,c4, Ta1, Ta2, Ta3, Ta4, Tb1, Tb2, Tb3, Tb4=basic_FU.Init_env(Env)

 
 Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4=rebond_corner(a,b,c,d,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4)


# Ta1.randomize(),Tb1.randomize()
# Ta2.randomize(),Tb2.randomize()
# Ta3.randomize(),Tb3.randomize()
# Ta4.randomize(),Tb4.randomize()
# print 'hi' 
 
 if Corner_method is 'CTM':
  c1, c2,c3,c4,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4=corner_transfer_matrix_twosite(a,b,c,d,chi,c1, c2,c3,c4,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4,D)
 if Corner_method is 'CTMRG':
  c1, c2,c3,c4,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4=corner_transfer_matrix_twosite_CTMRG(a,b,c,d,chi,c1, c2,c3,c4,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4,D)
 if Corner_method is 'CTMFull':
  c1, c2,c3,c4,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4=corner_transfer_matrix_twosite_CTMFull(a,b,c,d,chi,c1, c2,c3,c4,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4,D)


 basic_FU.reconstruct_env(c1,c2,c3,c4, Ta1, Ta2, Ta3, Ta4, Tb1, Tb2, Tb3, Tb4,Env)

 E1, E2, E3, E4, E5, E6, E7, E8=basicA.produce_Env(a,b,c,d,c1, c2,c3,c4,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4,D,d_phys)

 if Model is "Heisenberg":
   H1=Heisenberg1(h[2])
 if Model is "Heisenberg_Z2":
   H1=Heisenberg1_Z2(h[2],d_phys)
 if Model is "Heisenberg_U1":
   H1=Heisenberg1_U1(h[2],d_phys)

 
 E=basicA.energy_cb(E1, E2, E3, E4, E5, E6, E7, E8, a, b, c,d, H1,c_u,b_u)

 return E


def Energy_acd(a_u,b_u,d_u,a,b,c,d,Env,D,h,d_phys,chi,Corner_method,Model):

 c1,c2,c3,c4, Ta1, Ta2, Ta3, Ta4, Tb1, Tb2, Tb3, Tb4=basic_FU.Init_env(Env)

 #Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4=rebond_corner(a,b,c,d,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4)


# Ta1.randomize(),Tb1.randomize()
# Ta2.randomize(),Tb2.randomize()
# Ta3.randomize(),Tb3.randomize()
# Ta4.randomize(),Tb4.randomize()
 
 
 if Corner_method is 'CTM':
  c1, c2,c3,c4,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4=corner_transfer_matrix_twosite(a,b,c,d,chi,c1, c2,c3,c4,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4,D)
 if Corner_method is 'CTMRG':
  c1, c2,c3,c4,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4=corner_transfer_matrix_twosite_CTMRG(a,b,c,d,chi,c1, c2,c3,c4,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4,D)
 if Corner_method is 'CTMFull':
  c1, c2,c3,c4,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4=corner_transfer_matrix_twosite_CTMFull(a,b,c,d,chi,c1, c2,c3,c4,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4,D)


 basic_FU.reconstruct_env(c1,c2,c3,c4, Ta1, Ta2, Ta3, Ta4, Tb1, Tb2, Tb3, Tb4,Env)

 E1, E2, E3, E4, E5, E6, E7, E8=basicB.produce_Env(a,b,c,d,c1, c2,c3,c4,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4,D,d_phys)

 if Model is "Heisenberg":
   H1=Heisenberg1(h[2])
 if Model is "Heisenberg_Z2":
   H1=Heisenberg1_Z2(h[2],d_phys)
 if Model is "Heisenberg_U1":
   H1=Heisenberg1_U1(h[2],d_phys)

 E=basicA.energy_ad(E1, E2, E3, E4, E5, E6, E7, E8, a, b, c,d, H1,a_u,d_u)
 return E

def produce_Env_Hab(a,b,c,d,c1, c2,c3,c4,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4,D,d_phys):

 c1.setLabel([0,1])
 Tb1.setLabel([1,2,-2,3])
 E1=c1*Tb1
 E1.permute([0,2,-2,3],2)
 E1.setLabel([7,3,-3,8])
 E1.permute([7,3,-3,8],3)
 
 c2.setLabel([1,0])
 Ta1.setLabel([3,2,-2,1])
 E6=c2*Ta1
 E6.permute([0,2,-2,3],2)
 E6.setLabel([9,6,-6,8])
 E6.permute([8,6,-6,9],4)
 
 E5=Ta2
 E5.setLabel([10,5,-5,9])
 E5.permute([10,5,-5,9],3)
 
 E2=Tb4
 E2.setLabel([12,13,-13,7])
 E2.permute([12,13,-13,7],1)

 
 c3.setLabel([8,7])
 Tb2.setLabel([7,15,-15,22])
 Tb3.setLabel([13,14,-14,8])
 d.setLabel([16,-16,14,-14,15,-15,23,-23])
 E4=(((c3*Tb3)*Tb2)*d)
 E4.permute([13,16,-16,23,-23,22],3)
 E4.setLabel([11,16,-16,4,-4,10])
 E4.permute([11,16,-16,4,-4,10],3)


 
 c4.setLabel([11,10])
 Ta4.setLabel([11,17,-17,18])
 Ta3.setLabel([10,12,-12,13])
 c.setLabel([17,-17,12,-12,16,-16,19,-19])
 E3=(((c4*Ta4)*Ta3)*c)
 E3.permute([13,16,-16,19,-19,18],0)
 E3.setLabel([11,16,-16,1,-1,12])

 return E1, E2, E3, E4, E5,E6
 
def putBlock_Total(E1,E2):
    blk_qnums = E1.blockQnum()
    for qnum in blk_qnums:
        A=E1.getBlock(qnum)
        E2.putBlock(qnum,A)
    return E2
 
 

def  test_energy(E1, E2, E3, E4, E5,E6, a, b, c1,c2,c3,c4,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4, a_u,b_u,U):

 a_u.setLabel([20,13,1,2,3])
 a_d=copy.copy(a_u)
 a_d.transpose()
 a_d.setLabel([-2,-3,20,-13,-1])

 b_u.setLabel([40,2,4,5,6])
 b_d=copy.copy(b_u)
 b_d.transpose()
 b_d.setLabel([-5,-6,40,-2,-4])
 A=(((E2*(a_u*a_d))*E1)*E3)*(((((b_u*b_d)*E5)*E6)*E4))
 Norm_f=A


 a_u.setLabel([20,13,1,2,3])
 a_d.setLabel([-2,-3,-20,-13,-1])

 b_u.setLabel([40,2,4,5,6])
 b_d.setLabel([-5,-6,-40,-2,-4,])


 U.setLabel([-20,-40,20,40])



 B=((((E2*(a_u*a_d))*E1)*E3)*U)*(((((b_u*b_d)*E5)*E6)*E4))

 return B[0]/A[0]

def test_env(E1, E2, E3, E4, E5,E6, a, b, c1, c2,c3,c4,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4):
 a.setLabel([13,-13,1,-1,2,-2,3,-3])
 b.setLabel([2,-2,4,-4,5,-5,6,-6])
 A=(((E2*a)*E1)*E3)*((((b*E5)*E6)*E4))
 print 'NormEnv=', A[0]

def produce_Env_Hac(a,b,c,d,c1, c2,c3,c4,Ta1, Tb1,Ta2, Tb2,Ta3, Tb3,Ta4, Tb4,D,d_phys):

 c1.setLabel([0,1])
 Tb4.setLabel([3,2,-2,0])
 E2=c1*Tb4
 E2.permute([3,2,-2,1],3)
 E2.setLabel([10,2,-2,12])
 E2.setLabel([8,6,-6,9])
 E2.permute([8,6,-6,9],3)
 
 c4.setLabel([0,1])
 Ta3.setLabel([1,2,-2,3])
 E4=c4*Ta3
 E4.permute([0,2,-2,3],2)
 E4.setLabel([9,6,-6,8])
 E4.setLabel([7,13,-13,12])
 E4.permute([12,13,-13,7],1)
 
 E1=Tb1
 E1.setLabel([12,1,-1,13])
 E1.setLabel([9,5,-5,10])
 E1.permute([10,5,-5,9],3)

 E3=Ta4
 E3.setLabel([9,5,-5,10])
 E3.setLabel([7,3,-3,8])
 E3.permute([7,3,-3,8],3)
 
 
 c2.setLabel([5,6])
 Ta1.setLabel([21,20,-20,5])
 Ta2.setLabel([22,19,-19,6])
 b.setLabel([4,-4,23,-23,19,-19,20,-20])
 E6=(((c2*Ta2)*Ta1)*b)
 #E6.combineBond([23,22])
 E6.permute([21,4,-4,23,-23,22],4)
 E6.setLabel([13,3,-3,11,-11,22])
 E6.setLabel([10,4,-4,11,-11,22])
 E6.permute([11,-11,22,4,-4,10],3)
 
 
 
 c3.setLabel([8,7])
 Tb2.setLabel([7,15,-15,22])
 Tb3.setLabel([13,14,-14,8])
 d.setLabel([16,-16,14,-14,15,-15,23,-23])
 E5=(((c3*Tb3)*Tb2)*d)
 #E5.combineBond([23,22])
 E5.permute([13,16,-16,23,-23,22],4)
 E5.setLabel([8,7,-7,11,-11,22])
 E5.setLabel([12,1,-1,11,-11,22])
 E5.permute([11,-11,22,1,-1,12],0)
 return E1, E2, E3, E4, E5,E6
 
 
 
def reorder_env(E1, E2, E3, E4, E5,E6):

 E5p=copy.copy(E1)
 E6p=copy.copy(E2)
 E1p=copy.copy(E3)
 E2p=copy.copy(E4)
 E3p=copy.copy(E5)
 E4p=copy.copy(E6)
 return E1p,E2p,E3p,E4p,E5p,E6p

def Store(hlist,zlist, zlist1,zlist2,Elist, Elist1 , Elist2 , file):
 Length=len(zlist)-1
 file.write( str(hlist[Length]) + " " + str(zlist[Length]) +  " "+str(zlist1[Length])+" "+str(zlist2[Length])+" "+ str(Elist[Length])+" "+ str(Elist1[Length]) +" "+ str(Elist2[Length]) +  "\n")
 file.flush()


def Def_deltaNiter(i,N_iterF,Steps):
  delta=int(0.00)
  N_iter=int(0.00)


#  if 1.00e0>=Steps[0]>1.00e-1:
#   Steps[0]=Steps[0]-Steps[1]
#   N_iter=N_iterF
#   if Steps[0] <= 0 :Steps[0]=1.00e-1;

  if 1.00e-1>=Steps[0]>1.00e-2: 
    Steps[0]=Steps[0]-Steps[1]
    if Steps[0] < 1.00e-12:Steps[0]=1.00e-2;    
    N_iter=N_iterF

  if 1.00e-2>=Steps[0]>1.00e-3:
    Steps[0]=Steps[0]-Steps[2]
    #print "hi", Steps[0], Steps[2]
    N_iter=N_iterF
    if Steps[0] < 1.00e-12:Steps[0]=1.00e-3;    

  if 1.00e-3>=Steps[0]>1.00e-4:
    Steps[0]=Steps[0]-Steps[3]
    N_iter=N_iterF
    if Steps[0] < 1.00e-12:Steps[0]=1.00e-4;    

  if 1.00e-4>=Steps[0]>1.00e-5:
    Steps[0]=Steps[0]-Steps[4]
    N_iter=N_iterF
    if Steps[0] < 1.00e-12:Steps[0]=1.00e-5;    

  if 1.00e-5>=Steps[0]>1.00e-6:
    Steps[0]=Steps[0]-Steps[5]
    N_iter=N_iterF
    #print "hi0", Steps[0] 
    if Steps[0] <1.00e-12:Steps[0]=1.00e-6;    

  #print "hi1", Steps[0], Steps[len(Steps)-1], Steps[0] < Steps[len(Steps)-1]
  if Steps[0] < Steps[len(Steps)-1] or (Steps[0] < 1.00e-12):
   Steps[0]=int(0.00)
   N_iter=int(0.00)

  return Steps[0], N_iter









  







def Store(hlist,zlist, zlist1,zlist2,Elist, Elist1 , Elist2 , file):
 Length=len(zlist)-1
 file.write( str(hlist[Length]) + " " + str(zlist[Length]) +  " "+str(zlist1[Length])+" "+str(zlist2[Length])+" "+ str(Elist[Length])+" "+ str(Elist1[Length]) +" "+ str(Elist2[Length]) +  "\n")
 file.flush()

def Store_itebd(Gamma_a,Gamma_b,Gamma_c,Gamma_d,Landa_1,Landa_2,Landa_3,Landa_4,Landa_5, Landa_6, Landa_7,Landa_8):
 Gamma_a.save("Store/Gamma_a")
 Gamma_b.save("Store/Gamma_b")
 Gamma_c.save("Store/Gamma_c")
 Gamma_d.save("Store/Gamma_d")
 Landa_1.save("Store/Landa_1")
 Landa_2.save("Store/Landa_2")
 Landa_3.save("Store/Landa_3")
 Landa_4.save("Store/Landa_4")
 Landa_5.save("Store/Landa_5")
 Landa_6.save("Store/Landa_6")
 Landa_7.save("Store/Landa_7")
 Landa_8.save("Store/Landa_8")

def Reload_itebd():
 Gamma_a=uni10.UniTensor("Store/Gamma_a")
 Gamma_b=uni10.UniTensor("Store/Gamma_b")
 Gamma_c=uni10.UniTensor("Store/Gamma_c")
 Gamma_d=uni10.UniTensor("Store/Gamma_d")
 Landa_1=uni10.UniTensor("Store/Landa_1")
 Landa_2=uni10.UniTensor("Store/Landa_2")
 Landa_3=uni10.UniTensor("Store/Landa_3")
 Landa_4=uni10.UniTensor("Store/Landa_4")
 Landa_5=uni10.UniTensor("Store/Landa_5")
 Landa_6=uni10.UniTensor("Store/Landa_6")
 Landa_7=uni10.UniTensor("Store/Landa_7")
 Landa_8=uni10.UniTensor("Store/Landa_8")
 return Gamma_a,Gamma_b,Gamma_c,Gamma_d,Landa_1,Landa_2,Landa_3,Landa_4,Landa_5, Landa_6, Landa_7,Landa_8

def Store_Full(a_u,b_u,c_u,d_u,a,b,c,d):
 a_u.save("Store/a_u")
 b_u.save("Store/b_u")
 c_u.save("Store/c_u")
 d_u.save("Store/d_u")
 a.save("Store/a")
 b.save("Store/b")
 c.save("Store/c")
 d.save("Store/d")

def Store_Fullp(a_u,b_u,c_u,d_u,a,b,c,d):
 a_u.save("Store/ap_u")
 b_u.save("Store/bp_u")
 c_u.save("Store/cp_u")
 d_u.save("Store/dp_u")
 a.save("Store/ap")
 b.save("Store/bp")
 c.save("Store/cp")
 d.save("Store/dp")

def Reload_Fullp():
 ap_u=uni10.UniTensor("Store/ap_u")
 bp_u=uni10.UniTensor("Store/bp_u")
 cp_u=uni10.UniTensor("Store/cp_u")
 dp_u=uni10.UniTensor("Store/dp_u")
 ap=uni10.UniTensor("Store/ap")
 bp=uni10.UniTensor("Store/bp")
 cp=uni10.UniTensor("Store/cp")
 dp=uni10.UniTensor("Store/dp")
 return ap_u,bp_u,cp_u,dp_u,ap,bp,cp,dp


def Reload_Full():
 a_u=uni10.UniTensor("Store/a_u")
 b_u=uni10.UniTensor("Store/b_u")
 c_u=uni10.UniTensor("Store/c_u")
 d_u=uni10.UniTensor("Store/d_u")
 a=uni10.UniTensor("Store/a")
 b=uni10.UniTensor("Store/b")
 c=uni10.UniTensor("Store/c")
 d=uni10.UniTensor("Store/d")
 return a_u,b_u,c_u,d_u,a,b,c,d
def Rand_env_total(Env):
 Env1=copy.copy(Env)
 for i in xrange(len(Env1)):
  Env1[i]=copy.copy(Env[i])
  Env1[i].randomize()
 
 return  Env1


def qr_parity(theta):


    bd1=uni10.Bond(uni10.BD_IN,theta.bond(4).Qlist())
    bd2=uni10.Bond(uni10.BD_IN,theta.bond(5).Qlist())
    
    GA=uni10.UniTensor([theta.bond(0),theta.bond(1),theta.bond(2),theta.bond(3),theta.bond(4),theta.bond(5)])
    LA=uni10.UniTensor([bd1,bd2, theta.bond(4),theta.bond(5)])

    svds = {}
    blk_qnums = theta.blockQnum()
    dim_svd=[]

    for qnum in blk_qnums:
        svds[qnum] = theta.getBlock(qnum).qr()
        GA.putBlock(qnum, svds[qnum][0])
        LA.putBlock(qnum, svds[qnum][1])

#    print LA
    return GA, LA
    
def lq_parity(theta):

    bd1=uni10.Bond(uni10.BD_OUT,theta.bond(0).Qlist())
    bd2=uni10.Bond(uni10.BD_OUT,theta.bond(1).Qlist())
    GA=uni10.UniTensor([theta.bond(0),theta.bond(1),theta.bond(2),theta.bond(3),theta.bond(4),theta.bond(5)])
    LA=uni10.UniTensor([theta.bond(0),theta.bond(1),bd1,bd2])
    svds = {}
    blk_qnums = theta.blockQnum()
    dim_svd=[]
    for qnum in blk_qnums:
        svds[qnum] = theta.getBlock(qnum).lq()
        GA.putBlock(qnum, svds[qnum][1])
        LA.putBlock(qnum, svds[qnum][0])

#    print LA
    return  LA, GA




def Decomposition(U):

 H=copy.copy(U)
 H.setLabel([0,1,2,3,4,5])
 H.permute([0,3,4,5,2,1],2)
 
 l,q=lq_parity(H)
 l.setLabel([0,3,-1,-2])

 q.setLabel([-1,-2,4,5,2,1])
 q.permute([-1,-2,4,1,5,2],4)
 qq, r=qr_parity(q)
 qq.setLabel([-1,-2,4,1,-3,-4])
 r.setLabel([-3,-4,5,2]) 
 
 l.permute([0,-1,-2,3],1)
 qq.permute([-1,-2,1,-4,-3,4],3)
 r.permute([-3,-4,2,5],3)
 

 

 
 MPO_list=[]
 MPO_list.append(l)
 MPO_list.append(qq)
 MPO_list.append(r)

 H1=MPO_list[0]*MPO_list[1]*MPO_list[2]

 H1.permute([0,1,2,3,4,5],3)

 #print "Test", H1.elemCmp(U), MPO_list[0],MPO_list[1],MPO_list[2]
 return MPO_list
def slighty_random(a_u,b_u,c_u,d_u,a,b,c,d):
 rand=copy.copy(a_u)
 rand.randomize()
 a_u=a_u+(0.2)*rand

 rand=copy.copy(b_u)
 rand.randomize()
 b_u=b_u+(0.2)*rand
 
 rand=copy.copy(c_u)
 rand.randomize()
 c_u=c_u+(0.2)*rand
 
 rand=copy.copy(d_u)
 rand.randomize()
 d_u=d_u+(0.2)*rand


 a_u=a_u*(1.00/MaxAbs(a_u)) 
 b_u=b_u*(1.00/MaxAbs(b_u)) 
 c_u=c_u*(1.00/MaxAbs(c_u)) 
 d_u=d_u*(1.00/MaxAbs(d_u)) 
 
 a=make_ab(a_u)
 b=make_ab(b_u)
 c=make_ab(c_u)
 d=make_ab(d_u)
 
 return a_u,b_u,c_u,d_u,a,b,c,d

def total_random(a_u,b_u,c_u,d_u,a,b,c,d):
 a_u.randomize()
 b_u.randomize()
 c_u.randomize()
 d_u.randomize()


 a_u=a_u*(1.00/MaxAbs(a_u)) 
 b_u=b_u*(1.00/MaxAbs(b_u)) 
 c_u=c_u*(1.00/MaxAbs(c_u)) 
 d_u=d_u*(1.00/MaxAbs(d_u)) 
 
 a=make_ab(a_u)
 b=make_ab(b_u)
 c=make_ab(c_u)
 d=make_ab(d_u)
 
 return a_u,b_u,c_u,d_u,a,b,c,d


def max_ten(a):

 if ( MaxAbs(a) < 0.50e-1) or (MaxAbs(a) > 0.50e+1)   :
  a=a*(1.00/MaxAbs(a));
 else: a=a;
 
 return a


 