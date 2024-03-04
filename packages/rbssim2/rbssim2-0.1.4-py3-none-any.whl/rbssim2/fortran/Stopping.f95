subroutine inverse(E, lenE, params, lenParams, result)
    
        USE OMP_LIB
        
        integer :: lenE, lenParams
        real(8):: E(lenE), result(lenE), params(lenParams), tmplnE
!f2py   intent (in) E, lenE, lenParams, params
!f2py   intent (out) result
!f2py   depend(lenE) E
!f2py   depend(lenParams) params
!f2py   depend(lenE) result

!$OMP PARALLEL
        do i = 1, lenE

            tmplnE = log(E(i))
            result(i) = params(1) + params(2) * tmplnE + &
            params(3) * tmplnE ** 2 + params(4) * tmplnE ** 3 + &
            params(5) * tmplnE ** 4
        enddo
!$OMP END PARALLEL 

end

subroutine equation(E, lenE, params, lenParams, result)
    
    USE OMP_LIB
    
    integer :: lenE, lenParams
    real(8) :: E(lenE), result(lenE), params(lenParams), tmplnE
!f2py   intent (in) E, lenE, lenParams, params
!f2py   intent (out) result
!f2py   depend(lenE) E
!f2py   depend(lenParams) params
!f2py   depend(lenE) result

!$OMP PARALLEL
    do i = 1, lenE

        tmplnE = log(E(i))
        result(i) = 1. / (params(1) + params(2) * tmplnE + &
        params(3) * tmplnE ** 2 + params(4) * tmplnE ** 3 + &
        params(5) * tmplnE ** 4)
    enddo
!$OMP END PARALLEL 

end


subroutine inverseIntegral(E, lenE, params, lenParams, result)
    
    USE OMP_LIB
    
    integer :: lenE, lenParams
    real(8) :: E(lenE), result(lenE), params(lenParams), lnE, c1
!f2py   intent (in) E, lenE, lenParams, params
!f2py   intent (out) result
!f2py   depend(lenE) E
!f2py   depend(lenParams) params
!f2py   depend(lenE) result

    c1 = params(2) - 2.*params(3) + 6.*params(4) - 24.*params(5)
!$OMP PARALLEL
    do i = 1, lenE

        lnE = log(E(i))
        result(i) = E(i)*((params(1) - c1) + params(5) * lnE * lnE * lnE * lnE + &
        (params(4) - 4.*params(5)) * lnE * lnE * lnE + &
        (params(3) - 3.*params(4) + 12.*params(5)) * lnE * lnE + &
        c1*lnE)

    enddo
!$OMP END PARALLEL 

end


subroutine inverseIntegrate(E0, E1, lenE, params, lenParams, result)
    
    USE OMP_LIB
    
    integer :: lenE, lenParams
    real(8) :: result(lenE)
    real(8) :: E0(lenE), E1(lenE), result0(lenE), result1(lenE), params(lenParams)
!f2py   intent (in) E0, E1, lenE, lenParams, params
!f2py   intent (out) result
!f2py   depend(lenE) E0, E1
!f2py   depend(lenParams) params
!f2py   depend(lenE) result

    call inverseIntegral(E0, lenE, params, lenParams, result0)
    call inverseIntegral(E1, lenE, params, lenParams, result1)

!$OMP PARALLEL
    do i = 1, lenE

        result(i) = result0(i) - result1(i)
    
    enddo
!$OMP END PARALLEL

end

subroutine inverseDiff(E, lenE, params, lenParams, result)
    
    USE OMP_LIB
    
    integer :: lenE, lenParams
    real(8) :: E(lenE), result(lenE), params(lenParams), lnE
!f2py   intent (in) E, lenE, lenParams, params
!f2py   intent (out) result
!f2py   depend(lenE) E
!f2py   depend(lenParams) params
!f2py   depend(lenE) result

!$OMP PARALLEL
    do i = 1, lenE

        lnE = log(E(i))
        result(i) = (params(2) + 2. * params(3) * lnE + &
        3. * params(4) * lnE * lnE + 4. * params(5) * lnE * lnE * lnE) / E(i)
    enddo
!$OMP END PARALLEL

end



subroutine energyafterstopping(E0, X, lenE, params, lenParams, threshold, result)
    
    USE OMP_LIB
    
    integer :: lenE, lenParams
    real(8) :: E0(lenE), X(lenE), result(lenE), params(lenParams)
    real(8) :: int_from(lenE), tmp(1), val, energyend(1), threshold
    logical :: isend
!f2py   intent (in) E0, X, lenE, lenParams, params, threshold
!f2py   intent (out) result
!f2py   depend(lenE) E0, X
!f2py   depend(lenParams) params
!f2py   depend(lenE) result
    energyend(1) = 0
    isend = .false.

    call inverseIntegral(E0, lenE, params, lenParams, int_from)

!$OMP PARALLEL
    do i = 1, lenE
        energyend(1) = E0(i)
        if (isend) exit

        do j = 1, 100
            if (energyend(1) .le. threshold) then
                result(i) = 0
                isend = .true.
                exit
            endif

            call inverseIntegral(energyend, 1, params, lenParams, tmp)
            val =  int_from(i) - tmp(1) - X(i)
            
            if (abs(val) .le. 2e-2) then
                result(i) = energyend(1)
                exit
            endif
            
            call inverse(energyend, 1, params, lenParams, tmp)
            energyend(1) = energyend(1) + val / tmp(1)
        enddo
    enddo
!$OMP END PARALLEL

end