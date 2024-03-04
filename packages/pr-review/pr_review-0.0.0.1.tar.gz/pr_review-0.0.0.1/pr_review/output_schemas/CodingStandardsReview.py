from typing import Optional
from langchain_core.pydantic_v1 import BaseModel, Field



'''
check_coding_standardsの出力形式を定義, このモデルを元に生成される出力形式の指示文を{format_instruction}に渡す
'''
class CodingStandardsReview(BaseModel):
    NoChangeExternalAPIs: Optional[bool]  = Field(default=None, description="Check for true or false: When adding parameters to an existing API function, instead of modifying the existing function, create a new extended function (e.g., f_ex(a, b)). This ensures backward compatibility.")
    DescriptionNoChangeExternalAPIs: str  = Field(description="description for validation result of NoChangeExternalAPIs")

    StackUsageManagement: Optional[bool] = Field(description="Check for true or false: If a function uses more than 100 bytes of stack, apply the WOLFSSL_SMALL_STACK pattern to dynamically allocate variables and keep stack usage under 100 bytes per function.")
    DescriptionStackUsageManagement: str = Field(description="description for validation result of StackUsageManagement")

    FunctionShouldReturnValue: Optional[bool] = Field(default=None, description="Check for true or false: All functions should return a value.  No void function returns.  If a return is later added propagating the error checking upstream can become very complicated.")
    DescriptionFunctionShouldReturnValue: str = Field(description="description for validation result of FunctionShouldReturnValue")

    NoRecursion: Optional[bool] = Field(default=None, description="Check for true or false: No recursion, prefer iterative solutions.  Less stack use.")
    DescriptionNoRecursion: str = Field(description="description for validation result of NoRecursion")

    NoStandardLibAssumption: Optional[bool] = Field(default=None, description="Check for true or false: Whether the newly added code uses standard library functions instead of X macros.")
    DescriptionNoStandardLibAssumption: str = Field(description="description for validation result of NoStandardLibAssumption")

    CommentForEachFunction: Optional[bool] = Field(default=None, description="Check for true or false: Document each function with at least a one-line comment explaining the purpose and meaning of the return value.")
    DescriptionCommentForEachFunction: str = Field(description="description for validation result of CommentForEachFunction")

    UseForceZero: Optional[bool] = Field(default=None, description="Check for true or false: Use ForceZero() to zeroize private keys or sensitive data to prevent compiler optimizations from skipping memset at the end of functions.")
    DescriptionUseForceZero: str = Field(description="description for validation result of UseForceZero")

    DeclareVariablesOnTop: Optional[bool] = Field(default=None, description="Check for true or false: Declare variables at top of function unless only used in block scope. This Allows for variable declarations only.")
    DescriptionDeclareVariablesOnTop: str = Field(description="description for validation result of DeclareVariablesOnTop")

    StructMemberOrder: Optional[bool] = Field(default=None, description="Order struct members by its size in descending order, with unsigned bit-fields at the end of the structure.")
    DescriptionStructMemberOrder: str = Field(description="description for validation result of StructMemberOrder")

    ## Style

    Indentation: Optional[bool] = Field(default=None, description="Check for true or false: Use 4 spaces for indentation.")       
    DescriptionIndentation: str = Field(description="description for validation result of Indentation")

    # 80文字超えてないのにFalseになる
    MaxLineLength: Optional[bool] = Field(default=None, description="Check for true or false: Limit lines to a maximum of 80 characters.")
    DescriptionMaxLineLength: str = Field(description="description for validation result of MaxLineLength")

    VariableNaming: Optional[bool] = Field(default=None, description="Check for true or false: Start variable names with a lowercase letter and use camel case for multiple words (e.g., counter, buffLen).")
    DescriptionVariableNaming: str = Field(description="description for validation result of VariableNaming")

    FunctionWithNoArgs: Optional[bool] = Field(default=None, description="Check for true or false: Functions with no arguments must have (void) in arg list.")
    DescriptionFunctionWithNoArgs: str = Field(description="description for validation result of FunctionWithNoArgs")
    

    FunctionNaming: Optional[bool] = Field(default=None, description="Check for true or false: Function Naming Convention: Use camel case for function names (e.g., DoBumpAgain), not allowed snake case(e.g., do_bump_again).")
    DescriptionFunctionNaming: str = Field(description="description for validation result of FunctionNaming")

    ConstantNaming: Optional[bool] = Field(default=None, description="Check for true or false: Write constant names in uppercase, separating words with underscores (e.g., MAX_SIZE).")
    DescriptionConstantNaming: str = Field(description="description for validation result of ConstantNaming")

    NoTypeNameInVariableName: Optional[bool] = Field(default=None, description="Check for true or false: Avoid including the type in variable names (e.g., use ptr instead of aLongPtr).")
    DescriptionNoTypeNameInVariableName: str = Field(description="description for validation result of NoTypeNameInVariableName")
     
    CommentStyle: Optional[bool] = Field(default=None, description="Check for true or false: Only use /* */ style like this: (/* comment */) for comment or documentation.")
    DescriptionCommentStyle: str = Field(description="description for validation result of CommentStyle")

    BraceStyle: Optional[bool] = Field(default=None, description="Check for true or false: Use K&R style for if statements, and always start braces on a new line for function definitions.")
    DescriptionBraceStyle: str = Field(description="description for validation result of BraceStyle")
