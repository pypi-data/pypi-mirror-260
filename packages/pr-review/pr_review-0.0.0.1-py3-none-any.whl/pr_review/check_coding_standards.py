import sys
import os
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field, validator
from langchain_openai import ChatOpenAI, OpenAI

from pr_review.definitions import ROOT_DIR 
from pr_review.config import settings
from pr_review.output_schemas import CodingStandardsReview
from pr_review.utils import get_file_contents

def main():
    if len(sys.argv) < 2:
        print('Usage: $ python pr_review/check_coding_standards.py <File...>')
        print('  ex)  $ python pr_review/check_coding_standards.py file1.txt file2.txt')
        sys.exit(2)

    # settingファイルに行ってlanguageなど設定を変更できる。
    if sys.argv[1] == '--show-config-path':
        print(os.path.join(ROOT_DIR, "pr_review/settings/check_coding_standards.toml"))
        sys.exit(0)

    # ファイル(複数)のソースコードをロードする.
    code_chunks = get_file_contents(sys.argv[1:])

    # TODO: settingファイルからOPENAI_API_KEYを読み込み
    llm = ChatOpenAI(model="gpt-4-1106-preview", temperature=0.0)

    prompt = ChatPromptTemplate.from_messages(messages=[
        ("system", settings.SYSTEM_TEMPLATE),
        ("user", settings.USER_TEMPLATE)
    ])

    parser = PydanticOutputParser(pydantic_object=CodingStandardsReview)

    chain = prompt | llm | parser



    # CodingStandardReview型のオブジェクトで受け取る
    # TODO: ユーザーが設定ファイルのテンプレートに変数を新しく追加したときに、このプログラムを触らなくてよくする
    result: CodingStandardsReview = chain.invoke({
        "language": settings.variables.language, 
        "coding_rules": settings.variables.coding_rules,
        "extra_instruction": settings.variables.extra_instruction,
        "format_instruction": parser.get_format_instructions(),
        "code_chunks": code_chunks
    
    })

    print('🧪 Coding Standard Validation:')
    print(f'🎯 NoChangeExternalAPIs: {result.NoChangeExternalAPIs}\n\t{result.DescriptionNoChangeExternalAPIs}')
    print(f'🎯 FunctionShouldReturnValue: {result.FunctionShouldReturnValue}\n\t{result.DescriptionFunctionShouldReturnValue}')
    print(f'🎯 NoRecursion: {result.NoRecursion}\n\t{result.DescriptionNoRecursion}')
    print(f'🎯 NoStandardLibAssumption: {result.NoStandardLibAssumption}\n\t{result.DescriptionNoStandardLibAssumption}')
    print(f'🎯 CommentForEachFunction: {result.CommentForEachFunction}\n\t{result.DescriptionCommentForEachFunction}')
    print(f'🎯 UseForceZero: {result.UseForceZero}\n\t{result.DescriptionUseForceZero}')
    print(f'🎯 DeclareVariablesOnTop: {result.DeclareVariablesOnTop}\n\t{result.DescriptionDeclareVariablesOnTop}')
    print(f'🎯 StructMemberOrder: {result.StructMemberOrder}\n\t{result.DescriptionStructMemberOrder}')

    ## Style
    print(f'🎯 Indentation: {result.Indentation}\n\t{result.DescriptionIndentation}')
    print(f'🎯 MaxLineLength: {result.MaxLineLength}\n\t{result.DescriptionMaxLineLength}')
    print(f'🎯 VariableNaming: {result.VariableNaming}\n\t{result.DescriptionVariableNaming}')
    print(f'🎯 FunctionNaming: {result.FunctionNaming}\n\t{result.DescriptionFunctionNaming}')
    print(f'🎯 FunctionWithNoArgs: {result.FunctionWithNoArgs}\n\t{result.DescriptionFunctionWithNoArgs}')    
    print(f'🎯 ConstantNaming: {result.ConstantNaming}\n\t{result.DescriptionConstantNaming}')
    print(f'🎯 CommentStyle: {result.CommentStyle}\n\t{result.DescriptionCommentStyle}')
    print(f'🎯 BraceStyle: {result.BraceStyle}\n\t{result.DescriptionBraceStyle}')



    

if __name__ == '__main__':
    main()
