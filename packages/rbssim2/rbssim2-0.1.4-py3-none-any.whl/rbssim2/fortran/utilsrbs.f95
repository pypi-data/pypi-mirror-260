
subroutine gauss(x, lenx, a, b, c, d,  newx)
    
         integer :: lenx
         real(8) :: x(lenx), newx(lenx)
         real(8) :: a, b, c, d
!f2py    intent(in) x, a, b, c, d, lenx
!f2py    intent(out) newx
!f2py    depend(lenx) x, newx


!$OMP PARALLEL
    newx = a * exp( - 0.5 * ( x - b) ** 2 / (c ** 2)) + d
!$OMP END PARALLEL
    
end subroutine gauss


subroutine get_spread_responce(energies, spreads, size, kinfactor, matrix)

        integer :: size
        real(8) :: energies(size), newspreads(size), spreads(size), kinfactor
        real(8) :: matrix(size, size), row(size), a, d
        a = 1.
        d = 0.
!f2py   intent(in) energies, spreads, size, kinfactor
!f2py   intent(out) matrix
!f2py   depend(size) energies, spreads
        matrix(1, 1) = 1
        newspreads = spreads + spreads * kinfactor ** 2
        newspreads = sqrt(newspreads)

!$OMP PARALLEL
        do i = 2, size
            call gauss(energies, size, a, energies(i), newspreads(i), d, row)
            row = row / sum(row)
            matrix(i, :) = row
        enddo

end subroutine get_spread_responce


subroutine rutherford(energies, lene, z1, z2, m1, m2, theta, result)
        
        real(8), parameter :: pi = 3.1415926, c = 5.1837436e6
        integer, intent(in) :: lene
        real(8), intent(in) :: energies(lene)
        real(8), intent(in) :: z1, z2, m1, m2, theta
        real(8), intent(out) :: result(lene)
!f2py   intent(in) energies, lene, z1, z2, m1, m2, theta
!f2py   intent(out) matrix
!f2py  depend(lene) energies, result
        
        real(8) :: cost, sint
        real(8), dimension(:) :: a(lene), b(lene), d(lene)
        cost = cos(theta / 180. * pi)
        sint = sin(theta / 180. * pi)

        d = (z1 * z2 / energies) * (z1 * z2 / energies)
        A = sqrt(m2 * m2 - m1 * m1 * sint * sint) + m2 * cost
        B = m2 * sint * sint * sint * sint * sqrt(m2 * m2 - m1 * m1 * sint * sint)
        result = c * D * A * A / B
end subroutine rutherford