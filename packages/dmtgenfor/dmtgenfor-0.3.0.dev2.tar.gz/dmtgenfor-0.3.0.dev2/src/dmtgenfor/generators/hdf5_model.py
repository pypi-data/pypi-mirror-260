

from dmtgen.common.blueprint import Blueprint
from dmtgen.common.blueprint_attribute import BlueprintAttribute

from .common import to_type_name, to_field_name

H5_FUNCTION_TYPES = {"number": "Double", "double": "Double", "string": "String", "integer": "Integer"}

def create_hdf5_save(blueprint: Blueprint, attribute: BlueprintAttribute):
    """Create hdf5 save code"""
    name = attribute.name
    field_name = to_field_name(name)
    ftype = to_type_name(blueprint.name)

    def __primitive_save():
        atype = attribute.type
        if attribute.is_array:
            return __primitive_array_save()
        if atype == "boolean":
            return __boolean_save()
        if attribute.is_string:
            return f"""
            if (.not.(this%{field_name}%isEmpty())) then
                errorj = H5A_WriteStringWithLength(groupIndex, '{name}' // c_null_char, this%{field_name}%toChars() // c_null_char)
                if (H5A_IS_ERROR(errorj)) then
                    error_message = 'Error during saving of {name}'
                    call throw(io_exception(error_message))
                    return
                end if
            end if
            """
        f_name = H5_FUNCTION_TYPES[attribute.type]
        # TODO: Hvorfor brukes ikke en metode for å skrive til hdf5??
        return f"""
        if (allocated(this%{field_name}) then
            errorj = H5A_Write{f_name}(groupIndex, '{name}' // c_null_char,this%{field_name})
            if (H5A_IS_ERROR(errorj)) then
                error_message = 'Error during saving of {name}'
                call throw(io_exception(error_message))
                return
            end if
        end if
        """

    def __primitive_array_save():
        f_name = H5_FUNCTION_TYPES[attribute.type]
        # TODO: Dimensjoner som eget API!
        dims = attribute.dimensions
        ndim = len(dims)
        if ndim > 1:
            sdim = f"diml({ndim}:1:-1)"
        else:
            sdim = "diml"
        return f"""
        if (allocated(diml)) deallocate(diml)
        allocate(diml({ndim}),stat=sv)
        if (sv.ne.0) then
            errorj=-1
            error_message = 'Error during saving of {ftype}, error when trying to allocate diml&
                & array for {name}'
            call throw(illegal_state_exception(error_message%toChars()))
            return
        end if
        diml=shape(this%{name})
        errorj = H5A_Write{f_name}Array(groupIndex, '{name}' // c_null_char,{ndim},{sdim},this%{name})
        if (H5A_IS_ERROR(errorj)) then
            error_message = 'Error during saving of {name}'
            call throw(io_exception(error_message))
            return
        end if
        deallocate(diml)
        """


    def __boolean_save():
        return f"""
            if (this%{field_name}) then 
                logicalToIntSingle=1
            else
                logicalToIntSingle=0
            end if
            errorj = H5A_WriteInt(groupIndex, '{name}' // c_null_char,logicalToIntSingle)
            if (H5A_IS_ERROR(errorj)) then
                error_message = 'Error during saving of {name}'
                call throw(io_exception(error_message))
                return
            end if
            """

    def __entity_array_save():
        return f"""
        call orderList%destroy()
        if (allocated(this%{field_name})) then
            if (size(this%{field_name}) > 0) then
                if (allocated(diml)) deallocate(diml)
                allocate(diml(1),stat=sv)
                if (sv.ne.0) then
                    errorj=-1
                    error_message = 'Error during saving of {ftype}, error when trying to allocat&
                        &e diml array for body_array'
                    call throw(illegal_state_exception(error_message%toChars()))
                    return
                end if
                diml=shape(this%{field_name})
                subGroupIndex = H5A_OpenOrCreateEntity(groupIndex, '{name}' // c_null_char)
                do idx1 = 1,size(this%fieldname, 1)
                    if (this%{field_name}(idx1)%isValid()) then
                        str = '{name}_' // to_string(idx1)
                        subGroupIndex2 = H5A_OpenOrCreateEntity(subGroupIndex, str%toChars() // c_null_char)
                        call this%{field_name}(idx1)%save_hdf5(subGroupIndex2)
                        errorj=H5A_CloseEntity(subGroupIndex2)
                        if (exception_occurred()) return
                        if (.not.(orderList%isEmpty())) then
                            orderList=orderList+','
                        end if
                        orderList=orderList + str
                    end if
                end do
                errorj = H5A_writeStringWithLength(subGroupIndex, 'name' // c_null_char, '{attribute.description}' // c_null_char)
                if (H5A_IS_ERROR(errorj)) then
                    error_message = 'Error during saving of {name}'
                    call throw(io_exception(error_message))
                    return
                end if
                errorj = H5A_SetDim(subGroupIndex,size(diml,1), diml)
                if (H5A_IS_ERROR(errorj)) then
                    error_message = 'Error during saving of {name}'
                    call throw(io_exception(error_message))
                    return
                end if
                deallocate(diml)
                if (.not.(orderList%isEmpty())) then
                    errorj=h5a_setOrder(subGroupIndex,orderList%toChars() // c_null_char)
                    if (H5A_IS_ERROR(errorj)) then
                        error_message = 'Error during saving of {name}'
                        call throw(io_exception(error_message))
                        return
                    end if
                end if
                call orderList%destroy()
                errorj=H5A_CloseEntity(subGroupIndex)
            end if
        end if
        """

    def entity_single_save():
        if attribute.is_required:
            return f"""
            if (this%{name}%isValid()) then
                subGroupIndex = H5A_OpenOrCreateEntity(groupIndex, '{name}' // c_null_char)
                call this%{name}%save_HDF5(subGroupIndex)
                errorj=H5A_CloseEntity(subGroupIndex)
                if (exception_occurred()) return
            else
                error_message = 'Error during saving of {name}'        &
                    + ' - a non-optional object is invalid'
                call throw(io_exception(error_message))
                return
            end if
            """
        else:
            return f"""
            if(allocated(this%{name})) then
                if (this%{name}%isValid()) then
                    subGroupIndex = H5A_OpenOrCreateEntity(groupIndex, '{name}' // c_null_char)
                    call this%{name}%save_HDF5(subGroupIndex)
                    errorj=H5A_CloseEntity(subGroupIndex)
                    if (exception_occurred()) return
                else
                    error_message = 'Error during saving of {name}'        &
                    + ' - a non-optional object is invalid'
                    call throw(io_exception(error_message))
                    return
                end if
            end if
            """

    def __entity_save():
        if attribute.is_array:
            return __entity_array_save()
        return entity_single_save()

    if attribute.is_primitive:
        return __primitive_save()
    else:
        return __entity_save()


def create_hdf5_load(blueprint: Blueprint,attribute: BlueprintAttribute):
    """Create hdf5 load code"""
    name = attribute.name
    atype = attribute.type
    ftype = to_type_name(blueprint.name)
    field_name = to_field_name(name)

    def __primitive_single_load():
        if atype == "boolean":
            return __boolean_load()
        if atype == "string":
            return __string_load()

        h5_type = H5_FUNCTION_TYPES[atype]
        return f"""
        error = H5A_Read {h5_type}(groupIndex, '{name}' // c_null_char, this%{field_name})
        if (H5A_IS_ERROR(error)) then
            error_message = 'Error during loading of {ftype}' +        &
                    ' - failed to load property {name}'
            call throw(io_exception(error_message))
            return
        end if
        """

    def __primitive_array_load():
        dims = attribute.dimensions
        ndim = len(dims)
        h5_type = H5_FUNCTION_TYPES[atype]
        return f"""
        if (allocated(diml)) deallocate(diml)
        allocate(diml({ndim}),stat=sv)
        if (sv.ne.0) then
            error=-1
            error_message = 'Error during loading of {ftype}, error when trying to allocate dim&
                &l array for {name}'
            call throw(illegal_state_exception(error_message%toChars()))
            return
        end if
        error = H5A_GetArrayDims(groupIndex,'{name}' // c_null_char, diml)
        error = H5A_Read{h5_type}Array(groupIndex,'{name}' // c_null_char, this%{field_name})
        if (H5A_IS_ERROR(error)) then
            error_message = 'Error during loading of {ftype}' +        &
                    ' - failed to load property {name}'
            call throw(io_exception(error_message))
            return
        end if
        deallocate(diml)
        """

    def __boolean_load():
        return f"""
        error = H5A_ReadInt(groupIndex, '{name}' // c_null_char, logicalToIntSingle)
        if (H5A_IS_ERROR(error)) then
            error_message = 'Error during loading of {ftype}'        &        &
                    ' - failed to load property {name}'
            call throw(io_exception(error_message))
            return
        end if
        this%{field_name} = logicalToIntSingle == 1
        """

    def __string_load():
        return f"""
        error= H5A_getStringLength(groupIndex, '{name}' // c_null_char,strSize)
        if (error.ge.0) then
            if (allocated(cc_a)) deallocate(cc_a)
            allocate(character :: cc_a(strSize+1),stat=sv)
            if (sv.ne.0) then
                error=-1
                error_message = 'Error during loading of {ftype}.{name}'
                call throw(illegal_state_exception(error_message%toChars()))
                return
            end if
            error = H5A_ReadStringWithLength(groupIndex, '{name}' // c_null_char,cc_a)
            cc_a(strSize+1) = c_null_char
            this%{field_name}=String(cc_a)
            this%{field_name}=this%{name}%trim()
            deallocate(cc_a)
            if (H5A_IS_ERROR(error)) then
            error_message = 'Error during loading of {ftype}.{name}'
            call throw(io_exception(error_message))
                return
            end if
        end if
        """

    def __entity_array_load():
        # TODO: CLEANUP!!!
        return f"""
        call orderList%destroy()
        ! Open the array group
        subGroupIndex = H5A_OpenEntity(groupIndex,'{name}' // c_null_char)
        if (subGroupIndex.gt.0) then
            ! Read the order attribute
            error = H5A_GetOrderRank(subGroupIndex,orderRank)
            if (H5A_IS_ERROR(error)) then
                error_message = 'Error during reading of order rank of '        &
                        + ' property {name} for {ftype}'
                call throw(io_exception(error_message))
                return
            end if
            if (orderRank /= 1) then
                error_message = 'Error during loading of {ftype}'        &
                        + ' - order rank must be 1 for array {name}'
                call throw(io_exception(error_message))
                return
            end if
            error = H5A_GetOrderDim(subGroupIndex,orderDim)
            if (H5A_IS_ERROR(error)) then
                error_message = 'Error during loading of {ftype}'        &
                        + ' - order att. dimension could not be read for array: {name}'
                call throw(io_exception(error_message))
                return
            end if
            error = H5A_GetOrderSize(subGroupIndex,orderSize)
            if (H5A_IS_ERROR(error)) then
                error_message = 'Error during loading of {ftype}'        &
                        + ' - order not found for array {name}'
                call throw(io_exception(error_message))
                return
            end if
            if (orderDim(1).gt.1) then
                if (allocated(order_arr)) deallocate(order_arr)
                allocate(character :: order_arr(orderSize, orderDim(1)),stat=sv)
                if (sv.ne.0) then
                    error=-1
                    error_message = 'Error during loading of {ftype}, error when trying to alloca&
                        &te orderList for {name}'
                    call throw(illegal_state_exception(error_message%toChars()))
                    return
                end if
                error = H5A_GetOrderArray(subGroupIndex, order_arr)
                if (H5A_IS_ERROR(error)) then
                    error_message = 'Error during loading of {ftype} - '        &
                            + ' could not get array order of property {name}'
                    call throw(io_exception(error_message))
                    return
                end if
                if (allocated(listOfNames)) deallocate(listOfNames)
                allocate(listOfNames(orderDim(1)),stat=sv)
                if (sv.ne.0) then
                    error=-1
                    error_message = 'Error during loading of {ftype}, error when trying to alloca&
                        &te listOfNames for {name}'
                    call throw(illegal_state_exception(error_message%toChars()))
                    return
                end if
                if (allocated(cc_a)) deallocate(cc_a)
                allocate(character :: cc_a(orderSize+1),stat=sv)
                if (sv.ne.0) then
                    error=-1
                    error_message = 'Error during loading of {ftype}, error when trying to alloca&
                        &te orderList for {name}'
                    call throw(illegal_state_exception(error_message%toChars()))
                    return
                end if
                do ordInd=1,orderDim(1)
                    cc_a(1:orderSize)=order_arr(:,ordInd)
                    cc_a(orderSize+1)=c_null_char
                    listOfNames(ordInd)=String(cc_a)
                    listOfNames(ordInd) = listOfNames(ordInd)%trim()
                end do
                deallocate(order_arr)
            else
                if (allocated(cc_a)) deallocate(cc_a)
                allocate(character :: cc_a(orderSize+1),stat=sv)
                if (sv.ne.0) then
                    error=-1
                    error_message = 'Error during loading of {ftype}, error when trying to alloca&
                        &te orderList for {name}'
                    call throw(illegal_state_exception(error_message%toChars()))
                    return
                end if
                error = H5A_GetOrder(subGroupIndex, cc_a)
                if (H5A_IS_ERROR(error)) then
                    error_message = 'Error during loading of {ftype}'        &
                                 // ' - could not get order of property {name}'
                    call throw(io_exception(error_message))
                    return
                	end if
                cc_a(orderSize+1) = c_null_char
                orderList=String(cc_a)
                deallocate(cc_a)
                listOfNames = orderList%split(',')
            end if
            ! Read the arrDim attribute
            error = H5A_GetDimSize(subGroupIndex,arrDimSize)
            if (error < 0) then
                arrDimSize = 1
                error = 0
            end if
            if (arrDimSize /= 1) then
                    error_message = 'Error during loading of {ftype},'        &
                                   //' arrDim length is not consistent with the data model'        &
                                   //' for array: {name}'
                    call throw(io_exception(error_message))
                    return
            end if
            if (allocated(arrDim)) deallocate(arrDim)
            allocate(arrDim(arrDimSize),stat=sv)
            if (sv.ne.0) then
                error=-1
                error_message = 'Error during loading of {ftype}, error when trying to alloca&
                    &te arrDim array for {name}'
                call throw(illegal_state_exception(error_message%toChars()))
                return
            end if
            error = H5A_GetDim(subGroupIndex, arrDim)
            if (error < 0) then
                if (arrDimSize == 1) then 
                    arrDim(1) = size(listOfNames)
                    error = 0
                else
                    error_message = 'Error during loading of {ftype}'        &
                            + ' - arrDim was not found for array {name}'
                    call throw(io_exception(error_message))
                end if
            end if
            ! Allocate the array
            if (allocated(this%{field_name})) deallocate(this%{field_name})
            allocate(this%{field_name}(arrDim(1)),stat=sv)
            if (sv.ne.0) then
                error=-1
                error_message = 'Error during loading of {ftype}, error when trying to alloca&
                    &te {name}'
                call throw(illegal_state_exception(error_message%toChars()))
                return
            end if
            ! Read each component
            do idx=1,size(listOfNames)
                subGroupIndex2 = H5A_OpenEntity(subGroupIndex, listOfNames(idx)%toChars() // c_null_char)
                idxMod = idx
                idx1 = idxMod
                if (subGroupIndex2.gt.0) then
                    call this%{field_name}(idx1)%default_init(listOfNames(idx)%toChars())
                    call this%{field_name}(idx1)%load_HDF5(subGroupIndex2)
                    error=H5A_CloseEntity(subGroupIndex2)
                    if (exception_occurred()) return
                else
                    error_message = 'Error during loading of {ftype}'        &
                            + ' - group not found: ' // listOfNames(idx)%toChars()
                    call throw(io_exception(error_message))
                    return
                end if
            end do
            if (allocated(listOfNames)) deallocate(listOfNames)
        else
            allocate(this%{field_name}(0))
        end if
        call orderList%destroy()
        error=H5A_CloseEntity(subGroupIndex)
        """

    def __entity_single_load():
        return f"""
        subGroupIndex = H5A_OpenEntity(groupIndex,'{name}' // c_null_char)
        if (H5A_IS_ERROR(subGroupIndex)) then
            error_message = 'Error during loading of {ftype}'        &
                    + ' - failed to open property {name}'
            call throw(io_exception(error_message))
            return
        end if
        if (subGroupIndex>0) then
            call this%{field_name}%default_init('{name}')
            call this%{field_name}%load_HDF5(subGroupIndex)
            error=H5A_CloseEntity(subGroupIndex)
            if (exception_occurred()) return
        else
            error_message = 'Error during loading of {ftype}'        &
                    + ' - failed to open property {name}'
            call throw(io_exception(error_message))
            return
        end if
        """

    if attribute.is_primitive:
        if attribute.is_array:
            return __primitive_array_load()
        else:
            return __primitive_single_load()
    else:
        if attribute.is_array:
            return __entity_array_load()
        else:
            return __entity_single_load()


def create_save_order(blueprint: Blueprint):
    """Create save order code"""
    attr= blueprint.all_attributes
    res = "errorj = h5a_setOrder(groupIndex,'&\n"
    offset = "                    "
    for a in attr.values():
        res += f"{offset}{a.name},&\n"
    res += f"{offset}// c_null_char)"
    return res
