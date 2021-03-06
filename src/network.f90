!=======================================================================
!> @file network.f90
!> @brief chemical network module
!> @author P. Rivera, A. Rodriguez, A. Castellanos,  A. Raga and A. Esquivel
!> @date 4/May/2016

! Copyright (c) 2016 Guacho Co-Op
!
! This file is part of Guacho-3D.
!
! Guacho-3D is free software; you can redistribute it and/or modify
! it under the terms of the GNU General Public License as published by
! the Free Software Foundation; either version 3 of the License, or
! (at your option) any later version.
!
! This program is distributed in the hope that it will be useful,
! but WITHOUT ANY WARRANTY; without even the implied warranty of
! MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
! GNU General Public License for more details.
! You should have received a copy of the GNU General Public License
! along with this program.  If not, see http://www.gnu.org/licenses/.
!=======================================================================

!> @brief Chemical/atomic network module
!> @details this module should be generated by an interface code.

 module network

  implicit none

 ! number of species
  integer, parameter :: n_spec = 4

  ! number of equilibrium species
  integer, parameter:: nequil = 2

  ! number of total elements
  integer, parameter :: n_elem = 1

  ! number of non-equilibrium equations
  integer, parameter :: n_nequ = n_spec - nequil

  !  first index for the species in the global array
  integer, parameter :: n1_chem = 6 

  ! indexes of the different species
  integer, parameter :: H  = 1   ! H0
  integer, parameter :: HP = 2   ! H+
  integer, parameter :: H2 = 3   ! H_2
  integer, parameter :: ie = 4   ! n_e
  !   Integer, parameter :: iM  = n_spec+1

  ! indexes of the equilibrium species
  integer, parameter :: iHt = 1

  ! number of species with
  integer, parameter :: iHn = 3

  ! number of reaction rates
  integer, parameter :: n_reac = 8

  ! indexes of the different rates
  integer, parameter :: iR1 = 1
  integer, parameter :: iR2 = 2
  integer, parameter :: iR3 = 3
  integer, parameter :: iR4 = 4
  integer, parameter :: iR5 = 5
  integer, parameter :: iR6 = 6
  integer, parameter :: iR7 = 7
  integer, parameter :: iR8 = 8

 contains

!=======================================================================

subroutine derv(y,rate,dydt,y0)

  implicit none
  real (kind=8), intent(in)  ::   y0(n_elem)
  real (kind=8), intent(in)  ::    y(n_spec)
  real (kind=8), intent(out) :: dydt(n_spec)
  real (kind=8), intent(in)  :: rate(n_reac)

  dydt(h )= +2.*rate(ir1)*y(h2)*y(h2) + 2.*rate(ir2)*y(h2)*y(h)      &
            +2.*rate(ir3)*y(h2)*y(ie) -    rate(ir4)*y(h )*y(ie)     &
            +   rate(ir5)*y(hp)*y(ie) +    rate(ir6)*y(h2)           &
            +2.*rate(ir7)*y(h2)       -    rate(ir8)*y(h )*y0(iht)

  dydt(hp)= +   rate(ir4)*y(h )*y(ie) -    rate(ir5)*y(hp)*y(ie)     &
            +   rate(ir6)*y(h2)

  !conservation species
  dydt(h2)= - y0(iht) + y(h) + y(hp) + 2.*y(h2)
  dydt(ie)= - y(ie) + y(hp)

   end subroutine derv

!=======================================================================

subroutine get_jacobian(y,jacobian,rate)

  implicit none
  real (kind=8), intent(in)  :: y(n_spec)
  real (kind=8), intent(out) :: jacobian(n_spec,n_spec)
  real (kind=8), intent(in)  :: rate(n_reac)
  real :: yy0

  yy0=  y(h)+ y(hp) + 2.*y(h2)
  !h
  jacobian(h , h ) = +2.*rate(ir2)*y(h2) -    rate(ir4)*y(ie)   &
                     -   rate(ir8)*yy0
  jacobian(h , hp) = +   rate(ir5)*y(ie)
  jacobian(h , h2) = +4.*rate(ir1)*y(h2) + 2.*rate(ir2)*y(h )   &
                     +2.*rate(ir3)*y(ie) +    rate(ir6)         &
                     +2.*rate(ir7)
  jacobian(h , ie) = +2.*rate(ir3)*y(h2) -    rate(ir4)*y(h )   &
                     +   rate(ir5)*y(hp)
  !hp
  jacobian(hp, h ) = +   rate(ir4)*y(ie)
  jacobian(hp, hp) = -   rate(ir5)*y(ie)
  jacobian(hp, h2) = +   rate(ir6)
  jacobian(hp, ie) = +   rate(ir4)*y(h )  -   rate(ir5)*y(hp)
  !h2
  jacobian(h2, h ) =  1.d0
  jacobian(h2, hp) =  1.d0
  jacobian(h2, h2) =  2.d0
  jacobian(h2, ie) =  0.d0
  !e
  jacobian(ie, h ) =  0.d0
  jacobian(ie, hp) =  1.d0
  jacobian(ie, h2) =  0.d0
  jacobian(ie, ie) = -1.d0
end subroutine get_jacobian

!=======================================================================

subroutine get_reaction_rates(rate,T)
  implicit none
  real (kind=8) :: T,T300
  real (kind=8), dimension(n_reac),intent(out) ::rate

  T300=T/300.

  rate(iR1) = 1.e-8       * T300**0.e0     * exp(-8.41e4 /T)
  rate(iR2) = 4.67e-7     * T300**(-1.e0)  * exp(-5.5e4  /T)
  rate(iR3) = 3.22e-9     * T300**(0.35e0) * exp(-1.02e5 /T)
  rate(iR4) = 1.00978e-9  * T300**(0.5e0)  * exp(-1.578e5/T)
  rate(iR5) = 4.074746e-12* T300**(-0.79e0)* exp(-0.e0   /T)
  !rate(iR6) = 8.14d-17    * T300**(-0.5d0) * exp(-4.48d0 /T)
  rate(iR6) = 5.98e-18
  rate(iR7) = 1.3e-18
  if (T < 1000.) then
    rate(iR8)=5.2e-17*sqrt(T300)
  else
    rate(iR8)=0.
  end if

end subroutine get_reaction_rates

!=======================================================================

subroutine nr_init(y,y0)
  implicit none
  real, intent(out) :: y(n_spec)
  real, intent(in ) :: y0(n_elem)
  real :: yhi

  yhi=y0(iht)

  y(h)=yhi/2.
  y(hp)=yhi/2.
  y(h2)=(yhi/2.)/2.
  y(ie)=y(hp)

  return
end subroutine nr_init

!=======================================================================

logical function check_no_conservation(y,y0_in)
  implicit none
  real, intent(in)  :: y(n_spec)
  real, intent(in ) :: y0_in  (n_elem)
  real              :: y0_calc(n_elem)
  integer           :: i

  check_no_conservation = .false.

  y0_calc(iHt)=y(H)+y(Hp)+2.*y(H2)

  do i = 1, n_elem
    if ( y0_calc(i) > 1.0001*y0_in(i) ) check_no_conservation = .true.
  end do

end function check_no_conservation

!=======================================================================

end module network

!=======================================================================
