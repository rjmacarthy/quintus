from quintus import Quintus

quintus = Quintus()

quintus.add_local_model("llama-7b", "llama-7b-ft")

if __name__ == "__main__":
    quintus.chat("local")
