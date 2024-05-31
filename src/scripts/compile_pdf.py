from typeset import utils


for name, profile in utils.get_profiles().items():
    utils.create_pdf(name, profile)
