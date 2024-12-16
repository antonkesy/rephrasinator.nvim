if !has('python3')
    echomsg ':python3 is not available, rephrasinator.nvim will not be loaded.'
    finish
endif

python3 import rephrasinator_package.rephrasinator
python3 rephrasinator = rephrasinator_package.rephrasinator.Rephrasinator()

command! RephraseTest python3 rephrasinator.test()
