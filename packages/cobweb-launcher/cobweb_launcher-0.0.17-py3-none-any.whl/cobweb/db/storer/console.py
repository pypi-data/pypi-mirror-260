from cobweb import log, StorerInterface


class Console(StorerInterface):

    def store(self, data_list):
        for item in data_list:
            log.info(f"item info: {item}")

