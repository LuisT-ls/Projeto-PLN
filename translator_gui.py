import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from googletrans import Translator
import langdetect
import os
import pyperclip
import json
from datetime import datetime
import webbrowser
import textblob

class AdvancedTranslator:
    def __init__(self, history_file='translation_history.json'):
        self.translator = Translator()
        self.history_file = history_file
        self.history = self.load_history()
        self.supported_languages = {
            'en': 'English', 'es': 'Spanish', 'fr': 'French', 
            'de': 'German', 'it': 'Italian', 'pt': 'Portuguese', 
            'ru': 'Russian', 'ar': 'Arabic', 'zh-cn': 'Chinese (Simplified)', 
            'ja': 'Japanese', 'ko': 'Korean', 'hi': 'Hindi'
        }
    
    def detect_language(self, text):
        try:
            return langdetect.detect(text)
        except:
            return "Unknown"
    
    def translate(self, text, dest_lang='en', src_lang=None):
        try:
            if not src_lang:
                src_lang = self.detect_language(text)
            
            traducao = self.translator.translate(
                text, 
                dest=dest_lang, 
                src=src_lang
            )
            
            translation_entry = {
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'texto_original': text,
                'idioma_origem': src_lang,
                'texto_traduzido': traducao.text,
                'idioma_destino': dest_lang
            }
            
            self.save_to_history(translation_entry)
            
            return translation_entry
        
        except Exception as e:
            return {"error": str(e)}
    
    def get_language_choices(self):
        return [f"{code} ({name})" for code, name in self.supported_languages.items()]
    
    def text_analysis(self, text):
        try:
            blob = textblob.TextBlob(text)
            return {
                'word_count': len(blob.words),
                'sentiment': blob.sentiment.polarity,
                'subjectivity': blob.sentiment.subjectivity
            }
        except Exception as e:
            return {"error": str(e)}
    
    def load_history(self):
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except:
            return []
    
    def save_to_history(self, entry):
        self.history.append(entry)
        # Limitar histórico para últimas 100 traduções
        self.history = self.history[-100:]
        
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)
    
    def translate_file(self, file_path, dest_lang='en'):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            translated = self.translate(text, dest_lang)
            
            # Salvar arquivo traduzido
            save_path = file_path.rsplit('.', 1)[0] + f'_{dest_lang}_translated.txt'
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(translated['texto_traduzido'])
            
            return save_path
        except Exception as e:
            return str(e)

class TranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tradutor Multilíngue")
        self.root.geometry("900x850")
        self.root.configure(bg='#f0f0f0')
        
        self.translator = AdvancedTranslator()
        self.setup_ui()
    
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = ttk.Label(
            main_frame, 
            text="Tradutor Multilíngue", 
            font=("Arial", 18, "bold")
        )
        title_label.pack(pady=15)
        
        # Frame de entrada
        input_frame = ttk.LabelFrame(main_frame, text="Texto Original")
        input_frame.pack(fill=tk.X, pady=10)
        
        self.input_text = tk.Text(input_frame, height=8, width=70, wrap=tk.WORD)
        self.input_text.pack(padx=10, pady=10)
        
        # Frame de opções
        options_frame = ttk.Frame(main_frame)
        options_frame.pack(fill=tk.X, pady=10)
        
        # Idioma de origem
        ttk.Label(options_frame, text="Idioma Origem:").pack(side=tk.LEFT, padx=5)
        self.src_lang = ttk.Combobox(
            options_frame, 
            values=['Detectar Automaticamente'] + self.translator.get_language_choices(),
            width=25
        )
        self.src_lang.set('Detectar Automaticamente')
        self.src_lang.pack(side=tk.LEFT, padx=5)
        
        # Idioma de destino
        ttk.Label(options_frame, text="Idioma Destino:").pack(side=tk.LEFT, padx=5)
        self.dest_lang = ttk.Combobox(
            options_frame, 
            values=self.translator.get_language_choices(),
            width=25
        )
        self.dest_lang.set('en (English)')
        self.dest_lang.pack(side=tk.LEFT, padx=5)
        
        # Botões de ação
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=10)
        
        button_style = {'width': 15, 'padding': 5}
        
        ttk.Button(action_frame, text="Traduzir", command=self.translate_text, **button_style).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Copiar", command=self.copy_translation, **button_style).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Importar Arquivo", command=self.import_file, **button_style).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Análise de Texto", command=self.show_text_analysis, **button_style).pack(side=tk.LEFT, padx=5)
        
        # Frame de resultado
        result_frame = ttk.LabelFrame(main_frame, text="Texto Traduzido")
        result_frame.pack(fill=tk.X, pady=10)
        
        self.output_text = tk.Text(result_frame, height=8, width=70, wrap=tk.WORD, state='disabled')
        self.output_text.pack(padx=10, pady=10)
        
        # Frame de histórico
        history_frame = ttk.LabelFrame(main_frame, text="Histórico de Traduções")
        history_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Scrollbar para histórico
        history_scroll = ttk.Scrollbar(history_frame)
        history_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_list = tk.Listbox(
            history_frame, 
            height=5, 
            width=70, 
            yscrollcommand=history_scroll.set
        )
        self.history_list.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        history_scroll.config(command=self.history_list.yview)
        
        # Evento de clique duplo para ver detalhes do histórico
        self.history_list.bind('<Double-1>', self.show_history_details)
        
        # Botão de limpar histórico
        ttk.Button(main_frame, text="Limpar Histórico", command=self.clear_history).pack(pady=5)
    
    def translate_text(self):
        text = self.input_text.get("1.0", tk.END).strip()
        dest_lang = self.dest_lang.get().split()[0]
        src_lang = None if self.src_lang.get() == 'Detectar Automaticamente' else self.src_lang.get().split()[0]
        
        if not text:
            messagebox.showwarning("Aviso", "Por favor, insira um texto para traduzir.")
            return
        
        try:
            result = self.translator.translate(text, dest_lang, src_lang)
            
            self.output_text.config(state='normal')
            self.output_text.delete('1.0', tk.END)
            self.output_text.insert(tk.END, result['texto_traduzido'])
            self.output_text.config(state='disabled')
            
            self.update_history_list()
        except Exception as e:
            messagebox.showerror("Erro", str(e))
    
    def copy_translation(self):
        translation = self.output_text.get("1.0", tk.END).strip()
        if translation:
            pyperclip.copy(translation)
            messagebox.showinfo("Sucesso", "Tradução copiada para área de transferência!")
    
    def import_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Arquivos de Texto", "*.txt")]
        )
        if file_path:
            dest_lang = self.dest_lang.get().split()[0]
            try:
                save_path = self.translator.translate_file(file_path, dest_lang)
                messagebox.showinfo(
                    "Sucesso", 
                    f"Arquivo traduzido salvo em:\n{save_path}"
                )
            except Exception as e:
                messagebox.showerror("Erro", str(e))
    
    def update_history_list(self):
        self.history_list.delete(0, tk.END)
        for entry in reversed(self.translator.history):
            display_text = (
                f"{entry['timestamp']} | "
                f"{entry['idioma_origem']} → {entry['idioma_destino']}: "
                f"{entry['texto_original'][:30]}..."
            )
            self.history_list.insert(tk.END, display_text)
    
    def show_history_details(self, event):
        selection = self.history_list.curselection()
        if selection:
            index = selection[0]
            entry = list(reversed(self.translator.history))[index]
            
            details = (
                f"Timestamp: {entry['timestamp']}\n"
                f"Idioma Origem: {entry['idioma_origem']}\n"
                f"Idioma Destino: {entry['idioma_destino']}\n\n"
                f"Texto Original:\n{entry['texto_original']}\n\n"
                f"Texto Traduzido:\n{entry['texto_traduzido']}"
            )
            
            # Criar janela de detalhes
            details_window = tk.Toplevel(self.root)
            details_window.title("Detalhes da Tradução")
            details_window.geometry("600x500")
            
            details_text = tk.Text(details_window, wrap=tk.WORD)
            details_text.insert(tk.END, details)
            details_text.config(state='disabled')
            details_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    
    def clear_history(self):
        resposta = messagebox.askyesno("Confirmar", "Tem certeza que deseja limpar o histórico de traduções?")
        if resposta:
            self.translator.history = []
            with open(self.translator.history_file, 'w', encoding='utf-8') as f:
                json.dump([], f)
            self.update_history_list()
            messagebox.showinfo("Sucesso", "Histórico de traduções limpo.")
    
    def show_text_analysis(self):
        text = self.input_text.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Aviso", "Por favor, insira um texto para análise.")
            return
        
        try:
            analysis = self.translator.text_analysis(text)
            
            details = (
                f"Análise de Texto:\n"
                f"Número de Palavras: {analysis['word_count']}\n"
                f"Sentimento (Polaridade): {analysis['sentiment']:.2f}\n"
                f"Subjetividade: {analysis['subjectivity']:.2f}\n\n"
                "Interpretação:\n"
                "- Sentimento: -1 (Muito Negativo) a 1 (Muito Positivo)\n"
                "- Subjetividade: 0 (Objetivo) a 1 (Subjetivo)"
            )
            
            # Criar janela de análise
            analysis_window = tk.Toplevel(self.root)
            analysis_window.title("Análise de Texto")
            analysis_window.geometry("400x300")
            
            analysis_text = tk.Text(analysis_window, wrap=tk.WORD)
            analysis_text.insert(tk.END, details)
            analysis_text.config(state='disabled')
            analysis_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        except Exception as e:
            messagebox.showerror("Erro", str(e))

def main():
    root = tk.Tk()
    app = TranslatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()