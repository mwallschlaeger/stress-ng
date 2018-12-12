#
# Stress ng python bindings
# description: http://kernel.ubuntu.com/~cking/stress-ng/
#
import ctypes,os,logging

STRESS_NG_NAME = "STRESS_NG_BINDINGS"

''' structure used in stress-ng c code to run stress functions '''
class ARGS_T(ctypes.Structure):
	     _fields_ = [
	     			("counter", ctypes.POINTER(ctypes.c_uint64)), 	# stressor counter 
	                ("name", ctypes.POINTER(ctypes.c_char)), 		#  stressor name
	                ("max_ops", ctypes.c_uint64),					# max number of bogo ops 
	                ("instance", ctypes.c_uint32),					# stressor instance 
	                ("num_instances", ctypes.c_uint32),				# number of instances 
	                ("pid", ctypes.c_int),							# stressor pid 
	                ("ppid", ctypes.c_int),							# stressor ppid 
	                ("page_size", ctypes.c_size_t)					# page size 
	                ]

''' build ctypes char array from python string '''
def build_ctypes_char_array(string):
	string = str(string)
	return ctypes.create_string_buffer(bytes(string.encode("ascii")))

''' build ctypes ARGS_T struct required by stress-ng '''
def build_args_t(counter=1,name="",max_ops=1,instance=1,num_instances=1,do_print=False):
	args_t = ARGS_T(
					counter=ctypes.pointer(ctypes.c_uint64(counter)), 
					name=build_ctypes_char_array(name),
					max_ops=ctypes.c_uint64(max_ops),
					instance=ctypes.c_uint32(instance),
					num_instances=ctypes.c_uint32(num_instances),
					pid=ctypes.c_int(os.getpid()),
					ppid=ctypes.c_int(os.getppid()),
					page_size=stress_get_pagesize())
	c_args_t_p = ctypes.pointer(args_t)
	if do_print:
		print_args_t(c_args_t_p)
	return c_args_t_p

_stress_ng = ctypes.CDLL('../stress-ng.so')

####################
# helper functions #
####################

''' prints args_t struct in c (DEBUG) '''
_stress_ng.print_args_t.argstype = (ARGS_T)
def print_args_t(c_args_t_p):
	_stress_ng.print_args_t(c_args_t_p)

''' stress-ng get pagesize function '''
_stress_ng.stress_get_pagesize.argtype = (ctypes.c_void_p)
def stress_get_pagesize():
	result = _stress_ng.stress_get_pagesize(ctypes.c_void_p())
	return result


##################################
# stress cpu, cpu load functions #
##################################

''' available cpu methods in stress-ng c code '''
CPU_METHODS = [
		"ackermann",
		"bitops",
		"callfunc",
		"cdouble",
		"cfloat",
		"clongdouble",
		"correlate",
		"crc16",
		"decimal32",
		"decimal64",
		"decimal128",
		"dither",
		"djb2a",
		"double",
		"euler",
		"explog",
		"fibonacci",
		"fft",
		"float",
		"fnv1a",
		"gamma",
		"gcd",
		"gray",
		"hamming",
		"hanoi",
		"hyperbolic",
		"idct",
		"int8",
		"int16",
		"int32",
		"int64",
		"int128",
		"int32float",
		"int32double",
		"int32longdouble",
		"int64float",
		"int64double",
		"int64longdouble",
		"int128float",
		"int128double",
		"int128longdouble",
		"int128idecimal32",
		"int128idecimal64",
		"int128idecimal128",
		"jenkin",
		"jmp",
		"ln2",
		"longdouble",
		"loop",
		"maxtrixprod",
		"nsqrt",
		"omega",
		"parity",
		"phi",
		"pi",
		"pjw",
		"prime",
		"queens",
		"rand",
		"rgb",
		"sdbm",
		"trig",
		"zeta" ]
CPU_DEFAULT_METHOD = "nsqrt"

''' set cpu load in stress-ng c code '''
_stress_ng.stress_set_cpu_load.argtype = (ctypes.c_char_p)
def stress_set_cpu_load(load):
	result =_stress_ng.stress_set_cpu_load(build_ctypes_char_array(load))	
	return result

''' set cpu method in stress-ng c code '''
_stress_ng.stress_set_cpu_method.argtype = (ctypes.c_char_p)
def stress_set_cpu_method(method):
	result = _stress_ng.stress_set_cpu_method(build_ctypes_char_array(method))
	return result 

''' set method and load, check for parm failures'''
def prepare_stress_cpu(method,load=None):
	if method not in CPU_METHODS:
		logging.warning("{}: CPU-Method {} not available, using default method {}".format(STRESS_NG_NAME,method,CPU_DEFAULT_METHOD))
		method = CPU_DEFAULT_METHOD		
	if stress_set_cpu_method(method) is not 0:
		logging.warning("{}: Unable to set method {}".format(STRESS_NG_NAME,method))
		return None
	if load is not None:
		if stress_set_cpu_load(load) is not 0:
			logging.warning("{}: Unable to set load {}. Running with stress-ng.c default".format(STRESS_NG_NAME,load))
	return method

''' default stress_cpu function in stress-ng, non stop stress '''
_stress_ng.stress_cpu.argtype = (ARGS_T)
def stress_cpu(method,load=None,counter=1,max_ops=1,instance=1,num_instances=1,do_c_print=False):
	method = prepare_stress_cpu(method,load)
	if method is None:
		return 1

	c_args_t_p = build_args_t(counter=counter,
				 name=method,
				 max_ops=max_ops,
				 instance=instance,
				 num_instances=num_instances,
				 do_print=do_c_print)
	
	return _stress_ng.stress_cpu(c_args_t_p)	

''' one iteration of cpu stress method from cpu_method list '''
_stress_ng.ms_sim_stress_cpu.argtype = (ctypes.c_char_p)
def ms_sim_stress_cpu(method,load=None):
	method = prepare_stress_cpu(method,load)
	if method is None:
		return 1
	return _stress_ng.ms_sim_stress_cpu(build_ctypes_char_array(method))

################
# vm functions #
################
''' available vm methods in stress-ng c code '''
VM_METHODS = [
	"all",
	"flip",
	"galpat-0",
	"galpat-1",
	"gray",
	"incdec",
	"inc-nybble",
	"rand-set",
	"rand-sum",
	"ror",
	"swap",
	"move-inv",
	"modulo-x",
	"prime-0",
	"prime-1",
	"prime-gray-0",
	"prime-gray-1",
	"walk-0d",
	"walk-1d",
	"walk-0a",
	"walk-1a",
	"zero-one"
	]
VM_DEFAULT_METHOD = "zero-one"
VM_BYTES_DEFAULT = 4096 * 1000 # 4 MB

# not implemented yet, using defaults for now
#_stress_ng.stress_set_vm_flags.argtype(ctypes.c_int)
#_stress_ng.stress_set_vm_hang.argtype(ctypes.c_char_p)
#_stress_ng.stress_set_vm_madvise.argtype(ctypes.c_char_p)

''' set vm method in stress-ng c code '''
_stress_ng.stress_set_vm_method.argtype = (ctypes.c_char_p)
def stress_set_vm_method(method):
	return _stress_ng.stress_set_vm_method(build_ctypes_char_array(method))

''' set vm bytes used in stress-ng c code '''
_stress_ng.stress_set_vm_bytes.argtype = (ctypes.c_char_p)
def stress_set_vm_bytes(vm_bytes):
	vm_bytes = str(vm_bytes)
	return _stress_ng.stress_set_vm_bytes(build_ctypes_char_array(vm_bytes))

''' set method and vm-bytes, check for parm failures'''
def prepare_stress_vm(method,vm_bytes=None):
	if method not in VM_METHODS:
		logging.warning("{}: VM-Method {} not available, using default method {}".format(STRESS_NG_NAME,method,VM_DEFAULT_METHOD))
		method = VM_DEFAULT_METHOD		
	if stress_set_vm_method(method) is not 0:
		logging.warning("{}: Unable to set vm-method {}".format(STRESS_NG_NAME,method))
		return None
	if vm_bytes is None:
		vm_bytes = VM_BYTES_DEFAULT
	if stress_set_vm_bytes(vm_bytes) is not 0:
			logging.warning("{}: Unable to set vm-bytes {}. Running with stress-ng.c default".format(STRESS_NG_NAME,vm_bytes))
	return method

''' default stress_vm function in stress-ng, non stop stress '''
_stress_ng.stress_vm.argtype = (ARGS_T)
def stress_vm(method,vm_bytes=None,counter=1,max_ops=1,instance=1,num_instances=1,do_c_print=False):
	method = prepare_stress_vm(method,vm_bytes)
	if method is None:
		return 1

	c_args_t_p = build_args_t(counter=counter,
				 name=method,
				 max_ops=max_ops,
				 instance=instance,
				 num_instances=num_instances,
				 do_print=do_c_print)
	
	result = _stress_ng.stress_vm(c_args_t_p)
	return result

''' one iteration of vm stress method from vm_method list '''
_stress_ng.ms_sim_stress_vm.argtype = (ARGS_T)
def ms_sim_stress_vm(method,vm_bytes=None,counter=1,max_ops=1,instance=1,num_instances=1,do_c_print=False):
	method = prepare_stress_vm(method,vm_bytes)
	if method is None:
		return 1

	c_args_t_p = build_args_t(counter=counter,
				 name=method,
				 max_ops=max_ops,
				 instance=instance,
				 num_instances=num_instances,
				 do_print=do_c_print)
	
	result = _stress_ng.ms_sim_stress_vm(c_args_t_p)
	return result

#################
# mem functions #
#################

#_stress_ng.stress_set_malloc_max.argtype = (ctypes.c_char_p)
#_stress_ng.stress_malloc.argtype = (ARGS_T)
#_stress_ng.stress_set_malloc_bytes.argstype = (ctypes.c_char_p) 


#def stress_set_malloc_bytes(percent_mem):
#	result =_stress_ng.stress_set_malloc_bytes(ctypes.c_char_p(percent_mem.encode("utf-8")))	
#	return result

#def stress_set_malloc_max():
#	value = "132144"
#	result =_stress_ng.stress_set_malloc_max(value.encode("utf-8"))	


#def stress_malloc():
#	args_t = ARGS_T(0,0,1,3, 1, os.getpid(), os.getppid(),stress_get_pagesize())
#	result =_stress_ng.stress_malloc(args_t)	
#	return result 


