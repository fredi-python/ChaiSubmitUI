import gradio as gr
import chaiverse as chai
import yaml
from chaiverse.formatters import PromptFormatter


def submit_model(model_url, use_custom_formatter, memory_template, prompt_template, bot_template, user_template,
                 response_template, frequency_penalty, presence_penalty, stopping_words, temperature, top_k, top_p,
                 model_name,
                 reward_repo, best_of, max_input_tokens):
    config = {
        "model_repo": model_url,
        "generation_params": {
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty,
            "stopping_words": stopping_words.split(","),
            "temperature": temperature,
            "top_k": top_k,
            "top_p": top_p,
        },
        "model_name": model_name,
        "reward_repo": reward_repo,
        "best_of": best_of,
        "max_input_tokens": max_input_tokens
    }

    if use_custom_formatter:
        config["formatter"] = PromptFormatter(memory_template=memory_template, prompt_template=prompt_template,
                                              bot_template=bot_template, user_template=user_template,
                                              response_template=response_template)

    submitter = chai.ModelSubmitter()
    submission_id = submitter.submit(config)
    return submission_id


def save_config(model_url, use_custom_formatter, memory_template, prompt_template, bot_template,
                                  user_template, response_template, frequency_penalty, presence_penalty, stopping_words,
                                  temperature, top_k, top_p, model_name, reward_repo, best_of, max_input_tokens):

    config = {
        "model_repo": model_url,
        "generation_params": {
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty,
            "stopping_words": stopping_words,
            "temperature": temperature,
            "top_k": top_k,
            "top_p": top_p,
        },
        "model_name": model_name,
        "reward_repo": reward_repo,
        "best_of": best_of,
        "max_input_tokens": max_input_tokens,
    }

    if use_custom_formatter:
        config["use_custom_formatter"] = True
        config["formatter"] = {
            "memory_template": memory_template,
            "prompt_template": prompt_template,
            "bot_template": bot_template,
            "user_template": user_template,
            "response_template": response_template,
        }
    else:
        config["use_custom_formatter"] = False

    with open("config.yaml", "w") as f:
        yaml.dump(config, f)


def load_config(load_config_file):
    with open(load_config_file.name, "r") as f:
        content = f.read()

    config = yaml.load(content, Loader=yaml.FullLoader)

    list_of_return_values = [
        gr.Textbox(value=config["model_repo"], interactive=True),
        gr.Slider(value=config["generation_params"]["temperature"], interactive=True),
        gr.Slider(value=config["generation_params"]["frequency_penalty"], interactive=True),
        gr.Slider(value=config["generation_params"]["presence_penalty"], interactive=True),
        gr.Textbox(value=config["generation_params"]["stopping_words"], interactive=True),
        gr.Slider(value=config["generation_params"]["top_k"], interactive=True),
        gr.Slider(value=config["generation_params"]["top_p"], interactive=True),
        gr.Textbox(value=config["model_name"], interactive=True),
        gr.Textbox(value=config["reward_repo"], interactive=True),
        gr.Slider(value=config["best_of"], interactive=True),
        gr.Slider(value=config["max_input_tokens"], interactive=True),
        gr.Checkbox(value=config["use_custom_formatter"], interactive=True),
        gr.Textbox(value="", interactive=True),
        gr.Textbox(value="", interactive=True),
        gr.Textbox(value="", interactive=True),
        gr.Textbox(value="", interactive=True),
        gr.Textbox(value="", interactive=True),
    ]

    if not config["use_custom_formatter"]:
        return list_of_return_values

    list_of_return_values[12] = gr.Textbox(value=config["formatter"]["memory_template"], interactive=True)
    list_of_return_values[13] = gr.Textbox(value=config["formatter"]["prompt_template"], interactive=True)
    list_of_return_values[14] = gr.Textbox(value=config["formatter"]["bot_template"], interactive=True)
    list_of_return_values[15] = gr.Textbox(value=config["formatter"]["user_template"], interactive=True)
    list_of_return_values[16] = gr.Textbox(value=config["formatter"]["response_template"], interactive=True)

    return list_of_return_values


with gr.Blocks() as submit_page:
    gr.Label("""🚀 SubmitUI 🚀""")

    with gr.Row():
        with gr.Column():
            with gr.Group():
                model_url = gr.Textbox(lines=1, placeholder="Enter Huggingface model_id...", label="Model Url",
                                       interactive=True)

            with gr.Group():
                title = gr.Label("Formatter")
                use_custom_formatter = gr.Checkbox(label="Use Custom Formatter", interactive=True)
                memory_template = gr.Textbox(lines=1, placeholder="Enter memory template...", label="Memory Template",
                                             interactive=True)
                prompt_template = gr.Textbox(lines=1, placeholder="Enter prompt template...", label="Prompt Template",
                                             interactive=True)
                bot_template = gr.Textbox(lines=1, placeholder="Enter bot template...", label="Bot Template",
                                          interactive=True)
                user_template = gr.Textbox(lines=1, placeholder="Enter user template...", label="User Template",
                                           interactive=True)
                response_template = gr.Textbox(lines=1, placeholder="Enter response template...",
                                               label="Response Template", interactive=True)

            with gr.Group():
                frequency_penalty = gr.Slider(minimum=0, maximum=1, step=0.1, label="Frequency Penalty",
                                              interactive=True)
                presence_penalty = gr.Slider(minimum=0, maximum=1, step=0.1, label="Presence Penalty", interactive=True)
                stopping_words = gr.Textbox(lines=1, placeholder="Enter stopping words...",
                                            label="Stopping Words, seperate by comma", interactive=True)
                temperature = gr.Slider(minimum=0, maximum=2, step=0.1, label="Temperature", interactive=True)
                top_k = gr.Slider(minimum=0, maximum=100, step=1, label="Top K", interactive=True)
                top_p = gr.Slider(minimum=0, maximum=1, step=0.05, label="Top P", interactive=True)

            with gr.Group():
                model_name = gr.Textbox(lines=1, placeholder="Enter model name...", label="Model Name",
                                        interactive=True)
                reward_repo = gr.Textbox(lines=1, placeholder="Enter reward huggingface model_id...",
                                         label="Reward Repo", interactive=True)
                best_of = gr.Slider(minimum=0, maximum=16, step=1, label="Best Of", interactive=True)
                max_input_tokens = gr.Slider(minimum=0, maximum=1024, step=512, label="Max Input Tokens",
                                             interactive=True)

        with gr.Column():
            sub_id_output = gr.Textbox(label="STATUS", lines=14)

    submit = gr.Button("Submit")
    submit.click(submit_model,
                 inputs=[model_url, use_custom_formatter, memory_template, prompt_template, bot_template, user_template,
                         response_template, frequency_penalty, presence_penalty, stopping_words, temperature, top_k,
                         top_p, model_name, reward_repo, best_of, max_input_tokens], outputs=[sub_id_output])

    save_config_btn = gr.Button("Save Config")
    save_config_btn.click(save_config,
                          inputs=[model_url, use_custom_formatter, memory_template, prompt_template, bot_template,
                                  user_template, response_template, frequency_penalty, presence_penalty, stopping_words,
                                  temperature, top_k, top_p, model_name, reward_repo, best_of, max_input_tokens],
                          outputs=[])
    with gr.Group():
        load_config_file = gr.File()
        load_config_button = gr.Button("Load Config")
        load_config_button.click(load_config, inputs=[load_config_file],
                                 outputs=[model_url, temperature, frequency_penalty, presence_penalty, stopping_words, top_k, top_p, model_name, reward_repo, best_of, max_input_tokens, use_custom_formatter, memory_template, prompt_template, bot_template, user_template, response_template])


submit_page.launch()
