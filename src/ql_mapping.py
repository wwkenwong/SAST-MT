'''
Information preprocessed from the code in below comment section
'''

CodeQL_CWE_TO_TEST_CASE = {
"CWE-014" : ['cpp/ql/test/query-tests/Security/CWE/CWE-014/test.c', 'cpp/ql/test/query-tests/Security/CWE/CWE-014/test.cpp', 'cpp/ql/src/Security/CWE/CWE-014/MemsetMayBeDeleted-bad.c', 'cpp/ql/src/Security/CWE/CWE-014/MemsetMayBeDeleted-good.c'],
"CWE-022" : ['cpp/ql/test/query-tests/Security/CWE/CWE-022/SAMATE/TaintedPath/CWE23_Relative_Path_Traversal__char_console_fopen_11.cpp', 'cpp/ql/test/query-tests/Security/CWE/CWE-022/semmle/tests/test.c', 'cpp/ql/src/Security/CWE/CWE-022/TaintedPath.c'],
"CWE-078" : ['cpp/ql/test/query-tests/Security/CWE/CWE-078/SAMATE/ExecTainted/tests.cpp', 'cpp/ql/test/query-tests/Security/CWE/CWE-078/semmle/ExecTainted/test.cpp', 'cpp/ql/src/Security/CWE/CWE-078/ExecTainted.c'],
"CWE-079" : ['cpp/ql/test/query-tests/Security/CWE/CWE-079/semmle/CgiXss/search.c', 'cpp/ql/src/Security/CWE/CWE-079/CgiXss.c'],
"CWE-089" : ['cpp/ql/test/query-tests/Security/CWE/CWE-089/SqlTainted/test.c', 'cpp/ql/test/query-tests/Security/CWE/CWE-089/SqlTainted/test.cpp', 'cpp/ql/src/Security/CWE/CWE-089/SqlTainted.c'],
"CWE-114" : ['cpp/ql/test/query-tests/Security/CWE/CWE-114/SAMATE/UncontrolledProcessOperation/test.cpp', 'cpp/ql/test/query-tests/Security/CWE/CWE-114/semmle/UncontrolledProcessOperation/test.cpp', 'cpp/ql/src/Security/CWE/CWE-114/UncontrolledProcessOperation.c'],
"CWE-119" : ['cpp/ql/test/query-tests/Security/CWE/CWE-119/SAMATE/tests.cpp', 'cpp/ql/test/query-tests/Security/CWE/CWE-119/semmle/tests/overflowdestination.cpp', 'cpp/ql/test/query-tests/Security/CWE/CWE-119/semmle/tests/test_buffer_overrun.cpp', 'cpp/ql/test/query-tests/Security/CWE/CWE-119/semmle/tests/tests.cpp', 'cpp/ql/test/query-tests/Security/CWE/CWE-119/semmle/tests/tests_restrict.c', 'cpp/ql/test/query-tests/Security/CWE/CWE-119/semmle/tests/unions.cpp', 'cpp/ql/test/query-tests/Security/CWE/CWE-119/semmle/tests/var_size_struct.cpp', 'cpp/ql/src/Security/CWE/CWE-119/OverflowBuffer.c'],
"CWE-120" : ['cpp/ql/test/query-tests/Security/CWE/CWE-120/semmle/UnsafeUseOfStrcat/test.c', 'cpp/ql/test/query-tests/Security/CWE/CWE-120/semmle/tests/tests.c', 'cpp/ql/test/query-tests/Security/CWE/CWE-120/semmle/tests/tests2.cpp', 'cpp/ql/test/query-tests/Security/CWE/CWE-120/semmle/tests/unions.c', 'cpp/ql/test/query-tests/Security/CWE/CWE-120/semmle/tests/var_size_struct.cpp', 'cpp/ql/src/Security/CWE/CWE-120/BadlyBoundedWrite.c', 'cpp/ql/src/Security/CWE/CWE-120/OverrunWrite.c', 'cpp/ql/src/Security/CWE/CWE-120/OverrunWriteFloat.c', 'cpp/ql/src/Security/CWE/CWE-120/UnboundedWrite.c'],
"CWE-121" : ['cpp/ql/test/query-tests/Security/CWE/CWE-121/semmle/tests/more_tests.cpp', 'cpp/ql/test/query-tests/Security/CWE/CWE-121/semmle/tests/tests.c', 'cpp/ql/src/Security/CWE/CWE-121/UnterminatedVarargsCall.cpp'],
"CWE-129" : ['cpp/ql/test/query-tests/Security/CWE/CWE-129/SAMATE/ImproperArrayIndexValidation/CWE122_Heap_Based_Buffer_Overflow__c_CWE129_fgets_01.c', 'cpp/ql/test/query-tests/Security/CWE/CWE-129/semmle/ImproperArrayIndexValidation/test1.c', 'cpp/ql/src/Security/CWE/CWE-129/ImproperArrayIndexValidationBad.c', 'cpp/ql/src/Security/CWE/CWE-129/ImproperArrayIndexValidationGood.c'],
"CWE-131" : ['cpp/ql/test/query-tests/Security/CWE/CWE-131/semmle/NoSpaceForZeroTerminator/test.c', 'cpp/ql/test/query-tests/Security/CWE/CWE-131/semmle/NoSpaceForZeroTerminator/test.cpp', 'cpp/ql/test/query-tests/Security/CWE/CWE-131/semmle/NoSpaceForZeroTerminator/test2.cpp', 'cpp/ql/src/Security/CWE/CWE-131/NoSpaceForZeroTerminator.c'],
"CWE-134" : ['cpp/ql/test/query-tests/Security/CWE/CWE-134/SAMATE/char_connect_socket_w32_vsnprintf_01_bad.c', 'cpp/ql/test/query-tests/Security/CWE/CWE-134/SAMATE/char_console_fprintf_01_bad.c', 'cpp/ql/test/query-tests/Security/CWE/CWE-134/SAMATE/char_environment_fprintf_01_bad.c', 'cpp/ql/test/query-tests/Security/CWE/CWE-134/semmle/argv/argvLocal.c', 'cpp/ql/test/query-tests/Security/CWE/CWE-134/semmle/consts/consts.cpp', 'cpp/ql/test/query-tests/Security/CWE/CWE-134/semmle/funcs/funcsLocal.c', 'cpp/ql/test/query-tests/Security/CWE/CWE-134/semmle/globalVars/globalVars.c', 'cpp/ql/test/query-tests/Security/CWE/CWE-134/semmle/ifs/ifs.c', 'cpp/ql/src/Security/CWE/CWE-134/UncontrolledFormatString.c', 'cpp/ql/src/Security/CWE/CWE-134/UncontrolledFormatStringThroughGlobalVar.c'],
"CWE-190" : ['cpp/ql/test/query-tests/Security/CWE/CWE-190/SAMATE/examples.cpp', 'cpp/ql/test/query-tests/Security/CWE/CWE-190/semmle/ArithmeticUncontrolled/test.c', 'cpp/ql/test/query-tests/Security/CWE/CWE-190/semmle/ArithmeticUncontrolled/test.cpp', 'cpp/ql/test/query-tests/Security/CWE/CWE-190/semmle/ArithmeticWithExtremeValues/test.c', 'cpp/ql/test/query-tests/Security/CWE/CWE-190/semmle/ComparisonWithWiderType/test.c', 'cpp/ql/test/query-tests/Security/CWE/CWE-190/semmle/ComparisonWithWiderType/test2.c', 'cpp/ql/test/query-tests/Security/CWE/CWE-190/semmle/ComparisonWithWiderType/test3.cpp', 'cpp/ql/test/query-tests/Security/CWE/CWE-190/semmle/TaintedAllocationSize/field_conflation.c', 'cpp/ql/test/query-tests/Security/CWE/CWE-190/semmle/TaintedAllocationSize/test.cpp', 'cpp/ql/test/query-tests/Security/CWE/CWE-190/semmle/tainted/test.c', 'cpp/ql/test/query-tests/Security/CWE/CWE-190/semmle/tainted/test2.cpp', 'cpp/ql/test/query-tests/Security/CWE/CWE-190/semmle/tainted/test3.c', 'cpp/ql/test/query-tests/Security/CWE/CWE-190/semmle/tainted/test4.cpp', 'cpp/ql/test/query-tests/Security/CWE/CWE-190/semmle/tainted/test5.cpp', 'cpp/ql/test/query-tests/Security/CWE/CWE-190/semmle/tainted/test6.cpp', 'cpp/ql/src/Security/CWE/CWE-190/ArithmeticTainted.c', 'cpp/ql/src/Security/CWE/CWE-190/ArithmeticUncontrolled.c', 'cpp/ql/src/Security/CWE/CWE-190/ArithmeticWithExtremeValues.c', 'cpp/ql/src/Security/CWE/CWE-190/ComparisonWithWiderType.c', 'cpp/ql/src/Security/CWE/CWE-190/TaintedAllocationSize.c'],
"CWE-191" : ['cpp/ql/test/query-tests/Security/CWE/CWE-191/UnsignedDifferenceExpressionComparedZero/test.cpp', 'cpp/ql/src/Security/CWE/CWE-191/UnsignedDifferenceExpressionComparedZero.c'],
"CWE-197" : ['cpp/ql/test/query-tests/Security/CWE/CWE-197/SAMATE/IntegerOverflowTainted/tests.cpp'],
"CWE-242" : ['cpp/ql/test/query-tests/Security/CWE/CWE-242/semmle/tests/tests.cpp'],
"CWE-253" : ['cpp/ql/test/query-tests/Security/CWE/CWE-253/HResultBooleanConversion.c', 'cpp/ql/test/query-tests/Security/CWE/CWE-253/HResultBooleanConversion.cpp', 'cpp/ql/src/Security/CWE/CWE-253/HResultBooleanConversion.cpp'],
"CWE-290" : ['cpp/ql/test/query-tests/Security/CWE/CWE-290/semmle/AuthenticationBypass/test.cpp', 'cpp/ql/src/Security/CWE/CWE-290/AuthenticationBypass.cpp'],
"CWE-295" : ['cpp/ql/test/query-tests/Security/CWE/CWE-295/test.cpp', 'cpp/ql/test/query-tests/Security/CWE/CWE-295/test2.cpp', 'cpp/ql/src/Security/CWE/CWE-295/SSLResultConflationBad.cpp', 'cpp/ql/src/Security/CWE/CWE-295/SSLResultConflationGood.cpp', 'cpp/ql/src/Security/CWE/CWE-295/SSLResultNotCheckedBad.cpp', 'cpp/ql/src/Security/CWE/CWE-295/SSLResultNotCheckedGood.cpp'],
"CWE-311" : ['cpp/ql/test/query-tests/Security/CWE/CWE-311/semmle/tests/test.cpp', 'cpp/ql/test/query-tests/Security/CWE/CWE-311/semmle/tests/test2.cpp', 'cpp/ql/test/query-tests/Security/CWE/CWE-311/semmle/tests/test3.cpp', 'cpp/ql/src/Security/CWE/CWE-311/CleartextStorage.c'],
"CWE-319" : ['cpp/ql/test/query-tests/Security/CWE/CWE-319/UseOfHttp/test.cpp', 'cpp/ql/src/Security/CWE/CWE-319/UseOfHttp.cpp'],
"CWE-327" : ['cpp/ql/test/query-tests/Security/CWE/CWE-327/test.cpp', 'cpp/ql/test/query-tests/Security/CWE/CWE-327/test2.cpp', 'cpp/ql/src/Security/CWE/CWE-327/BrokenCryptoAlgorithm.c', 'cpp/ql/src/Security/CWE/CWE-327/OpenSslHeartbleed.c'],
"CWE-367" : ['cpp/ql/test/query-tests/Security/CWE/CWE-367/semmle/test.cpp', 'cpp/ql/test/query-tests/Security/CWE/CWE-367/semmle/test2.cpp', 'cpp/ql/src/Security/CWE/CWE-367/TOCTOUFilesystemRaceBad.c', 'cpp/ql/src/Security/CWE/CWE-367/TOCTOUFilesystemRaceGood.c'],
"CWE-416" : ['cpp/ql/test/query-tests/Security/CWE/CWE-416/semmle/tests/test.cpp'],
"CWE-428" : ['cpp/ql/test/query-tests/Security/CWE/CWE-428/UnsafeCreateProcessCall.cpp', 'cpp/ql/src/Security/CWE/CWE-428/UnsafeCreateProcessCall.cpp'],
"CWE-457" : ['cpp/ql/test/query-tests/Security/CWE/CWE-457/semmle/ConditionallyUninitializedVariable/examples.cpp', 'cpp/ql/test/query-tests/Security/CWE/CWE-457/semmle/ConditionallyUninitializedVariable/test.cpp', 'cpp/ql/test/query-tests/Security/CWE/CWE-457/semmle/tests/test.cpp', 'cpp/ql/src/Security/CWE/CWE-457/ConditionallyUninitializedVariableBad.c', 'cpp/ql/src/Security/CWE/CWE-457/ConditionallyUninitializedVariableGood.c'],
"CWE-468" : ['cpp/ql/test/query-tests/Security/CWE/CWE-468/semmle/IncorrectPointerScaling/test.cpp', 'cpp/ql/test/query-tests/Security/CWE/CWE-468/semmle/IncorrectPointerScaling/test_large.cpp', 'cpp/ql/test/query-tests/Security/CWE/CWE-468/semmle/IncorrectPointerScaling/test_small.cpp', 'cpp/ql/test/query-tests/Security/CWE/CWE-468/semmle/SuspiciousAddWithSizeof/test.cpp', 'cpp/ql/src/Security/CWE/CWE-468/IncorrectPointerScaling.cpp', 'cpp/ql/src/Security/CWE/CWE-468/IncorrectPointerScalingChar.cpp', 'cpp/ql/src/Security/CWE/CWE-468/IncorrectPointerScalingVoid.cpp', 'cpp/ql/src/Security/CWE/CWE-468/SuspiciousAddWithSizeof.cpp'],
"CWE-497" : ['cpp/ql/test/query-tests/Security/CWE/CWE-497/SAMATE/tests.c', 'cpp/ql/test/query-tests/Security/CWE/CWE-497/semmle/tests/tests2.cpp', 'cpp/ql/src/Security/CWE/CWE-497/ExposedSystemDataCorrect.cpp', 'cpp/ql/src/Security/CWE/CWE-497/ExposedSystemDataIncorrect.cpp'],
"CWE-570" : ['cpp/ql/test/query-tests/Security/CWE/CWE-570/test.cpp', 'cpp/ql/src/Security/CWE/CWE-570/IncorrectAllocationErrorHandling.cpp'],
"CWE-676" : ['cpp/ql/test/query-tests/Security/CWE/CWE-676/SAMATE/DangerousUseOfCin/test.cpp', 'cpp/ql/test/query-tests/Security/CWE/CWE-676/semmle/DangerousUseOfCin/test.cpp', 'cpp/ql/test/query-tests/Security/CWE/CWE-676/semmle/PotentiallyDangerousFunction/test.c', 'cpp/ql/src/Security/CWE/CWE-676/DangerousFunctionOverflow.c', 'cpp/ql/src/Security/CWE/CWE-676/DangerousUseOfCin.cpp', 'cpp/ql/src/Security/CWE/CWE-676/PotentiallyDangerousFunction.c'],
"CWE-704" : ['cpp/ql/test/query-tests/Security/CWE/CWE-704/WcharCharConversion.cpp', 'cpp/ql/src/Security/CWE/CWE-704/WcharCharConversion.cpp'],
"CWE-732" : ['cpp/ql/test/query-tests/Security/CWE/CWE-732/UnsafeDaclSecurityDescriptor.cpp', 'cpp/ql/src/Security/CWE/CWE-732/DoNotCreateWorldWritable.c', 'cpp/ql/src/Security/CWE/CWE-732/UnsafeDaclSecurityDescriptor.cpp'],
"CWE-764" : ['cpp/ql/test/query-tests/Security/CWE/CWE-764/semmle/tests/DiningPhilosophers.cpp', 'cpp/ql/test/query-tests/Security/CWE/CWE-764/semmle/tests/test.cpp', 'cpp/ql/src/Security/CWE/CWE-764/LockOrderCycleExample.cpp', 'cpp/ql/src/Security/CWE/CWE-764/TwiceLockedBad.cpp', 'cpp/ql/src/Security/CWE/CWE-764/TwiceLockedGood.cpp', 'cpp/ql/src/Security/CWE/CWE-764/UnreleasedLockBad.cpp', 'cpp/ql/src/Security/CWE/CWE-764/UnreleasedLockGood.cpp'],
"CWE-772" : ['cpp/ql/test/query-tests/Security/CWE/CWE-772/SAMATE/tests.cpp', 'cpp/ql/test/query-tests/Security/CWE/CWE-772/semmle/tests-file/test.cpp', 'cpp/ql/test/query-tests/Security/CWE/CWE-772/semmle/tests-memory/test.cpp'],
"CWE-807" : ['cpp/ql/test/query-tests/Security/CWE/CWE-807/semmle/TaintedCondition/test.cpp', 'cpp/ql/src/Security/CWE/CWE-807/TaintedCondition.c'],
"CWE-835" : ['cpp/ql/test/query-tests/Security/CWE/CWE-835/semmle/InfiniteLoopWithUnsatisfiableExitCondition/test.cpp', 'cpp/ql/src/Security/CWE/CWE-835/InfiniteLoopBad.c', 'cpp/ql/src/Security/CWE/CWE-835/InfiniteLoopGood.c'],
"CWE-020" : ['cpp/ql/src/Security/CWE/CWE-020/ExternalAPISinkExample.cpp', 'cpp/ql/src/Security/CWE/CWE-020/ExternalAPITaintStepExample.cpp'],
"CWE-170" : ['cpp/ql/src/Security/CWE/CWE-170/ImproperNullTerminationTaintedBad.cpp', 'cpp/ql/src/Security/CWE/CWE-170/ImproperNullTerminationTaintedGood.cpp'],
"CWE-313" : ['cpp/ql/src/Security/CWE/CWE-313/CleartextSqliteDatabase.c'],
}

CodeQL_CWE_TO_QL = {
"CWE-119" : ['cpp/ql/test/query-tests/Security/CWE/CWE-119/semmle/tests/varsize.ql', 'cpp/ql/src/Security/CWE/CWE-119/OverflowBuffer.ql'],
"CWE-457" : ['cpp/ql/test/query-tests/Security/CWE/CWE-457/semmle/tests/LoopConditionsConst.ql', 'cpp/ql/src/Security/CWE/CWE-457/ConditionallyUninitializedVariable.ql'],
"CWE-497" : ['cpp/ql/test/query-tests/Security/CWE/CWE-497/SAMATE/OutputWrite.ql', 'cpp/ql/test/query-tests/Security/CWE/CWE-497/semmle/tests/OutputWrite.ql', 'cpp/ql/src/Security/CWE/CWE-497/ExposedSystemData.ql'],
"CWE-014" : ['cpp/ql/src/Security/CWE/CWE-014/MemsetMayBeDeleted.ql'],
"CWE-020" : ['cpp/ql/src/Security/CWE/CWE-020/CountUntrustedDataToExternalAPI.ql', 'cpp/ql/src/Security/CWE/CWE-020/IRCountUntrustedDataToExternalAPI.ql', 'cpp/ql/src/Security/CWE/CWE-020/IRUntrustedDataToExternalAPI.ql', 'cpp/ql/src/Security/CWE/CWE-020/UntrustedDataToExternalAPI.ql'],
"CWE-022" : ['cpp/ql/src/Security/CWE/CWE-022/TaintedPath.ql'],
"CWE-078" : ['cpp/ql/src/Security/CWE/CWE-078/ExecTainted.ql'],
"CWE-079" : ['cpp/ql/src/Security/CWE/CWE-079/CgiXss.ql'],
"CWE-089" : ['cpp/ql/src/Security/CWE/CWE-089/SqlTainted.ql'],
"CWE-114" : ['cpp/ql/src/Security/CWE/CWE-114/UncontrolledProcessOperation.ql'],
"CWE-120" : ['cpp/ql/src/Security/CWE/CWE-120/BadlyBoundedWrite.ql', 'cpp/ql/src/Security/CWE/CWE-120/OverrunWrite.ql', 'cpp/ql/src/Security/CWE/CWE-120/OverrunWriteFloat.ql', 'cpp/ql/src/Security/CWE/CWE-120/UnboundedWrite.ql'],
"CWE-121" : ['cpp/ql/src/Security/CWE/CWE-121/UnterminatedVarargsCall.ql'],
"CWE-129" : ['cpp/ql/src/Security/CWE/CWE-129/ImproperArrayIndexValidation.ql'],
"CWE-131" : ['cpp/ql/src/Security/CWE/CWE-131/NoSpaceForZeroTerminator.ql'],
"CWE-134" : ['cpp/ql/src/Security/CWE/CWE-134/UncontrolledFormatString.ql', 'cpp/ql/src/Security/CWE/CWE-134/UncontrolledFormatStringThroughGlobalVar.ql'],
"CWE-170" : ['cpp/ql/src/Security/CWE/CWE-170/ImproperNullTerminationTainted.ql'],
"CWE-190" : ['cpp/ql/src/Security/CWE/CWE-190/ArithmeticTainted.ql', 'cpp/ql/src/Security/CWE/CWE-190/ArithmeticUncontrolled.ql', 'cpp/ql/src/Security/CWE/CWE-190/ArithmeticWithExtremeValues.ql', 'cpp/ql/src/Security/CWE/CWE-190/ComparisonWithWiderType.ql', 'cpp/ql/src/Security/CWE/CWE-190/IntegerOverflowTainted.ql', 'cpp/ql/src/Security/CWE/CWE-190/TaintedAllocationSize.ql'],
"CWE-191" : ['cpp/ql/src/Security/CWE/CWE-191/UnsignedDifferenceExpressionComparedZero.ql'],
"CWE-253" : ['cpp/ql/src/Security/CWE/CWE-253/HResultBooleanConversion.ql'],
"CWE-290" : ['cpp/ql/src/Security/CWE/CWE-290/AuthenticationBypass.ql'],
"CWE-295" : ['cpp/ql/src/Security/CWE/CWE-295/SSLResultConflation.ql', 'cpp/ql/src/Security/CWE/CWE-295/SSLResultNotChecked.ql'],
"CWE-311" : ['cpp/ql/src/Security/CWE/CWE-311/CleartextBufferWrite.ql', 'cpp/ql/src/Security/CWE/CWE-311/CleartextFileWrite.ql', 'cpp/ql/src/Security/CWE/CWE-311/CleartextTransmission.ql'],
"CWE-313" : ['cpp/ql/src/Security/CWE/CWE-313/CleartextSqliteDatabase.ql'],
"CWE-319" : ['cpp/ql/src/Security/CWE/CWE-319/UseOfHttp.ql'],
"CWE-327" : ['cpp/ql/src/Security/CWE/CWE-327/BrokenCryptoAlgorithm.ql', 'cpp/ql/src/Security/CWE/CWE-327/OpenSslHeartbleed.ql'],
"CWE-367" : ['cpp/ql/src/Security/CWE/CWE-367/TOCTOUFilesystemRace.ql'],
"CWE-428" : ['cpp/ql/src/Security/CWE/CWE-428/UnsafeCreateProcessCall.ql'],
"CWE-468" : ['cpp/ql/src/Security/CWE/CWE-468/IncorrectPointerScaling.ql', 'cpp/ql/src/Security/CWE/CWE-468/IncorrectPointerScalingChar.ql', 'cpp/ql/src/Security/CWE/CWE-468/IncorrectPointerScalingVoid.ql', 'cpp/ql/src/Security/CWE/CWE-468/SuspiciousAddWithSizeof.ql'],
"CWE-570" : ['cpp/ql/src/Security/CWE/CWE-570/IncorrectAllocationErrorHandling.ql'],
"CWE-676" : ['cpp/ql/src/Security/CWE/CWE-676/DangerousFunctionOverflow.ql', 'cpp/ql/src/Security/CWE/CWE-676/DangerousUseOfCin.ql', 'cpp/ql/src/Security/CWE/CWE-676/PotentiallyDangerousFunction.ql'],
"CWE-704" : ['cpp/ql/src/Security/CWE/CWE-704/WcharCharConversion.ql'],
"CWE-732" : ['cpp/ql/src/Security/CWE/CWE-732/DoNotCreateWorldWritable.ql', 'cpp/ql/src/Security/CWE/CWE-732/UnsafeDaclSecurityDescriptor.ql'],
"CWE-764" : ['cpp/ql/src/Security/CWE/CWE-764/LockOrderCycle.ql', 'cpp/ql/src/Security/CWE/CWE-764/TwiceLocked.ql', 'cpp/ql/src/Security/CWE/CWE-764/UnreleasedLock.ql'],
"CWE-807" : ['cpp/ql/src/Security/CWE/CWE-807/TaintedCondition.ql'],
"CWE-835" : ['cpp/ql/src/Security/CWE/CWE-835/InfiniteLoopWithUnsatisfiableExitCondition.ql'],
"CWE-416" : ['cpp/ql/src/Critical/UseAfterFree.ql']
}


MSFT_CHECKING ={
"CWE-665": ['cpp/ql/src/Likely Bugs/Memory Management/UninitializedLocal.ql'],
"CWE-121": ['cpp/ql/src/Security/CWE/CWE-121/UnterminatedVarargsCall.ql'],
"CWE-190": ['cpp/ql/src/Likely Bugs/Arithmetic/BadAdditionOverflowCheck.ql','cpp/ql/src/Security/CWE/CWE-190/ComparisonWithWiderType.ql', 'cpp/ql/src/Likely Bugs/Arithmetic/IntMultToLong.ql'],
"CWE-835": ['cpp/ql/src/Security/CWE/CWE-190/ComparisonWithWiderType.ql'],
"CWE-480": ['cpp/ql/src/Likely Bugs/Likely Typos/IncorrectNotOperatorUsage.ql'],
"CWE-843": ['cpp/ql/src/Likely Bugs/Conversion/CastArrayPointerArithmetic.ql'],
"CWE-468": ['cpp/ql/src/Security/CWE/CWE-468/SuspiciousAddWithSizeof.ql','cpp/ql/src/Likely Bugs/Memory Management/SuspiciousSizeof.ql','cpp/ql/src/Security/CWE/CWE-468/IncorrectPointerScaling.ql','cpp/ql/src/Security/CWE/CWE-468/IncorrectPointerScalingVoid.ql'],
"CWE-681": ['cpp/ql/src/Likely Bugs/Arithmetic/IntMultToLong.ql'],
"CWE-192": ['cpp/ql/src/Likely Bugs/Arithmetic/BadAdditionOverflowCheck.ql' ,'cpp/ql/src/Likely Bugs/Arithmetic/IntMultToLong.ql'],
"CWE-457": ['cpp/ql/src/Likely Bugs/Memory Management/UninitializedLocal.ql' ,'cpp/ql/src/Security/CWE/CWE-457/ConditionallyUninitializedVariable.ql'],
"CWE-119": ['cpp/ql/src/Likely Bugs/Conversion/CastArrayPointerArithmetic.ql'],
"CWE-704": ['cpp/ql/src/Security/CWE/CWE-704/WcharCharConversion.ql'],
"CWE-676": ['cpp/ql/src/Security/CWE/CWE-676/PotentiallyDangerousFunction.ql'],
"CWE-197": ['cpp/ql/src/Security/CWE/CWE-190/ComparisonWithWiderType.ql', 'cpp/ql/src/Likely Bugs/Arithmetic/IntMultToLong.ql'],
"CWE-253": ['cpp/ql/src/Security/CWE/CWE-253/HResultBooleanConversion.ql'],
}


MSFT_MUST_FIX = [
    "cpp/ql/src/Security/CWE/CWE-190/ComparisonWithWiderType.ql",
    "cpp/ql/src/Security/CWE/CWE-704/WcharCharConversion.ql",
    "cpp/ql/src/Security/CWE/CWE-253/HResultBooleanConversion.ql",
    "cpp/ql/src/Likely Bugs/Memory Management/PointerOverflow.ql",
    "cpp/ql/src/Likely Bugs/Arithmetic/BadAdditionOverflowCheck.ql",
    "cpp/ql/src/Likely Bugs/Underspecified Functions/TooFewArguments.ql",

]

MS_MUST_FIX_ISSUE_TO_QUERY = {
'cpp/too-few-arguments': "cpp/ql/src/Likely Bugs/Underspecified Functions/TooFewArguments.ql",
'cpp/bad-addition-overflow-check': "cpp/ql/src/Likely Bugs/Arithmetic/BadAdditionOverflowCheck.ql"	,
'cpp/pointer-overflow-check': "cpp/ql/src/Likely Bugs/Memory Management/PointerOverflow.ql",
'cpp/hresult-boolean-conversion': "cpp/ql/src/Security/CWE/CWE-253/HResultBooleanConversion.ql",
'cpp/incorrect-string-type-conversion': "cpp/ql/src/Security/CWE/CWE-704/WcharCharConversion.ql",
'cpp/comparison-with-wider-type': "cpp/ql/src/Security/CWE/CWE-190/ComparisonWithWiderType.ql",
}


# CodeQL CWE database
CODEQL = ['CWE-014', 'CWE-022', 'CWE-078', 'CWE-079', 'CWE-089', 'CWE-114', 'CWE-119', 'CWE-120', 
          'CWE-121', 'CWE-129', 'CWE-131', 'CWE-134', 'CWE-190', 'CWE-191', 'CWE-197', 'CWE-242', 
          'CWE-253', 'CWE-290', 'CWE-295', 'CWE-311', 'CWE-319', 'CWE-327', 'CWE-367', 'CWE-416', 
          'CWE-428', 'CWE-457', 'CWE-468', 'CWE-497', 'CWE-570', 'CWE-676', 'CWE-704', 'CWE-732', 
          'CWE-764', 'CWE-772', 'CWE-807', 'CWE-835']

# Juliet samples
JULIET = ['CWE-789', 'CWE-484', 'CWE-194', 'CWE-563', 'CWE-588', 'CWE-078', 'CWE-390', 'CWE-364', 
          'CWE-226', 'CWE-188', 'CWE-127', 'CWE-775', 'CWE-780', 'CWE-667', 'CWE-843', 'CWE-587', 
          'CWE-480', 'CWE-259', 'CWE-762', 'CWE-400', 'CWE-223', 'CWE-284', 'CWE-252', 'CWE-247', 
          'CWE-620', 'CWE-479', 'CWE-535', 'CWE-176', 'CWE-676', 'CWE-459', 'CWE-377', 'CWE-690', 
          'CWE-590', 'CWE-191', 'CWE-325', 'CWE-190', 'CWE-835', 'CWE-615', 'CWE-672', 'CWE-440', 
          'CWE-681', 'CWE-561', 'CWE-122', 'CWE-482', 'CWE-123', 'CWE-481', 'CWE-244', 'CWE-426', 
          'CWE-468', 'CWE-475', 'CWE-571', 'CWE-591', 'CWE-272', 'CWE-197', 'CWE-391', 'CWE-328', 
          'CWE-464', 'CWE-196', 'CWE-469', 'CWE-338', 'CWE-319', 'CWE-476', 'CWE-195', 'CWE-467', 
          'CWE-511', 'CWE-124', 'CWE-680', 'CWE-396', 'CWE-114', 'CWE-397', 'CWE-036', 'CWE-606', 
          'CWE-416', 'CWE-483', 'CWE-134', 'CWE-415', 'CWE-562', 'CWE-427', 'CWE-404', 'CWE-500', 
          'CWE-546', 'CWE-273', 'CWE-242', 'CWE-015', 'CWE-506', 'CWE-510', 'CWE-398', 'CWE-785', 
          'CWE-367', 'CWE-526', 'CWE-773', 'CWE-023', 'CWE-090', 'CWE-327', 'CWE-605', 'CWE-685', 
          'CWE-570', 'CWE-321', 'CWE-832', 'CWE-401', 'CWE-256', 'CWE-457', 'CWE-126', 'CWE-121', 
          'CWE-666', 'CWE-675', 'CWE-534', 'CWE-253', 'CWE-688', 'CWE-366', 'CWE-617', 'CWE-369', 
          'CWE-674', 'CWE-758', 'CWE-222', 'CWE-478', 'CWE-761', 'CWE-665']

# CWE can be detected
# It is derived from MS's doc and what presents in CodeQL's CWE folder 
CWE_DETECT = ['CWE-843', 'CWE-428', 'CWE-665', 'CWE-457', 'CWE-114', 'CWE-681', 'CWE-295', 'CWE-190', 'CWE-468', 
              'CWE-732', 'CWE-570', 'CWE-131', 'CWE-367', 'CWE-835', 'CWE-120', 'CWE-319', 'CWE-327', 'CWE-772', 
              'CWE-416', 'CWE-191', 'CWE-089', 'CWE-290', 'CWE-480', 'CWE-129', 'CWE-497', 'CWE-704', 'CWE-807', 
              'CWE-014', 'CWE-192', 'CWE-119', 'CWE-134', 'CWE-121', 'CWE-253', 'CWE-764', 'CWE-197', 'CWE-079', 
              'CWE-242', 'CWE-311', 'CWE-676', 'CWE-078', 'CWE-022']


JULIET_TO_CHECK = ['CWE-843', 'CWE-242', 'CWE-197', 'CWE-665', 'CWE-570', 'CWE-681', 'CWE-114', 'CWE-078', 
                   'CWE-253', 'CWE-457', 'CWE-319', 'CWE-835', 'CWE-134', 'CWE-480', 'CWE-676', 'CWE-367', 
                   'CWE-416', 'CWE-468', 'CWE-190', 'CWE-327', 'CWE-121', 'CWE-191']


'''
import os 
import glob 


full_path = ''

def all_file_under_path(rootFolderPath):
    ret = []
    for root, dirs, files in os.walk(rootFolderPath):
        for filename in files:
            ret.append(full_path+os.path.join(root, filename))
    return ret 


s = glob.glob('*')

CodeQL_CWE_TO_TEST_CASE = {}

CodeQL_CWE_TO_QL = {}

for cwe in s:
    if cwe != 'README.md':
        ret = all_file_under_path(cwe)
        for file in ret:
            if file.endswith('.ql'):
                if cwe in CodeQL_CWE_TO_QL.keys():
                    CodeQL_CWE_TO_QL[cwe].append(file)
                else:
                    CodeQL_CWE_TO_QL[cwe] = [file]
            elif file.endswith('.c') or file.endswith('.cpp'):
                if cwe in CodeQL_CWE_TO_TEST_CASE.keys():
                    CodeQL_CWE_TO_TEST_CASE[cwe].append(file)
                else:
                    CodeQL_CWE_TO_TEST_CASE[cwe] = [file]

for key in CodeQL_CWE_TO_TEST_CASE.keys():
    print("\""+key+"\" : "+str(CodeQL_CWE_TO_TEST_CASE[key])+',')


for key in CodeQL_CWE_TO_QL.keys():
    print("\""+key+"\" : "+str(CodeQL_CWE_TO_QL[key])+',')

'''
