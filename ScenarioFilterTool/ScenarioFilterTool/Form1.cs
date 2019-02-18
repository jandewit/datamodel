using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace ScenarioFilterTool
{
    public partial class Form1 : Form
    {
        HashSet<string> target_words;
        JObject scenario;
        string prevOpenDir = null;
        string prevSaveDir = null;
        System.Random rnd = new System.Random();

        public Form1()
        {
            InitializeComponent();
            cbVariation.SelectedIndex = 0;
            cbPart.SelectedIndex = 0;
        }

        private void btnOpen_Click(object sender, EventArgs e)
        {
            if (prevOpenDir != null)
            {
                openFileDialog1.InitialDirectory = prevOpenDir;
            }

            DialogResult result = openFileDialog1.ShowDialog();

            if (result == DialogResult.OK)
            {
                prevOpenDir = Path.GetDirectoryName(openFileDialog1.FileName);

                this.LoadFile();

                // Fill the dropdown boxes
                cbTargetWord1.Items.Clear();
                cbTargetWord2.Items.Clear();
                cbTargetWord3.Items.Clear();
                cbTargetWord1.Items.AddRange(this.target_words.ToArray<string>());
                cbTargetWord2.Items.AddRange(this.target_words.ToArray<string>());
                cbTargetWord3.Items.AddRange(this.target_words.ToArray<string>());

                cbTargetWord1.SelectedIndex = 0;
                cbTargetWord2.SelectedIndex = 1;
                cbTargetWord3.SelectedIndex = 2;
            }
        }

        private void LoadFile()
        {
            this.target_words = new HashSet<string>();

            // Load the JSON file
            using (StreamReader r = new StreamReader(openFileDialog1.FileName))
            {
                string json = r.ReadToEnd();
                this.scenario = (JObject)JsonConvert.DeserializeObject(json);

                foreach (JObject t in scenario["tasks"])
                {
                    foreach (JObject s in t["subtasks"])
                    {
                        if (s["target_word"] != null)
                        {
                            // Figure out which target words are there in the JSON
                            this.target_words.Add((string)s["target_word"]["target_word"]);
                        }
                    }
                }
            }
        }

        private void btnSave_Click(object sender, EventArgs e)
        {
            if (prevSaveDir != null)
            {
                saveFileDialog1.InitialDirectory = prevSaveDir;
            }

            DialogResult result = saveFileDialog1.ShowDialog();

            if (result == DialogResult.OK)
            {
                // Remove all target words that are not relevant from the JSON
                for (int i = scenario["tasks"].Count() - 1; i >= 0; i--)
                {
                    JObject t = (JObject)scenario["tasks"][i];

                    List<JObject>[] modelSubtasks = new List<JObject>[3];
                    for (int x = 0; x < 3; x++)
                    {
                        modelSubtasks[x] = new List<JObject>();
                    }

                    string lastWord = "";
                    int currentIndex = -1;

                    // Remove all tasks that are not relevant
                    if (t["lang"] != null)
                    {
                        if ((cbVariation.SelectedIndex == 0 && (string)t["lang"] == "L1") || (cbVariation.SelectedIndex == 1 && (string)t["lang"] == "L2"))
                        {
                            ((JArray)scenario["tasks"]).Remove(t);
                        }
                    }

                    if (t["order"] != null)
                    {
                        if ((cbPart.SelectedIndex == 0 && (int)t["order"] != 1) || (cbPart.SelectedIndex == 1 && (int)t["order"] != 2))
                        {
                            ((JArray)scenario["tasks"]).Remove(t);
                        }
                    }

                    for (int j = t["subtasks"].Count() - 1; j >= 0; j--)
                    {
                        JObject s = (JObject)t["subtasks"][j];

                        if (s["target_word"] != null)
                        {
                            // Figure out which target words are there in the JSON
                            string word = (string)s["target_word"]["target_word"];
                            if ((cbVariation.SelectedIndex == 0 && (string)s["target_word"]["lang"] == "L1") || (cbVariation.SelectedIndex == 1 && (string)s["target_word"]["lang"] == "L2") || (word != (string)cbTargetWord1.Text && word != (string)cbTargetWord2.Text && word != (string)cbTargetWord3.Text))
                            {
                                ((JArray)t["subtasks"]).Remove(s);
                            }

                            else
                            {
                                if(word != lastWord)
                                {
                                    currentIndex++;
                                    lastWord = word;
                                }

                                modelSubtasks[currentIndex].Add(s);
                            }
                        }
                    }

                    if (modelSubtasks[0].Count > 0)
                    {
                        int[] indices = Enumerable.Range(0, 3).OrderBy(r => rnd.Next()).ToArray();

                        JArray st = (JArray)t["subtasks"];
                        st.Clear();

                        for (int ii = 0; ii < 3; ii++)
                        {
                            for (int ist = modelSubtasks[indices[ii]].Count-1; ist >= 0; ist--)
                            {
                                st.Add(modelSubtasks[indices[ii]][ist]);
                            }
                        }
                    }
                }

                string newjson = JsonConvert.SerializeObject(scenario);
                using (StreamWriter w = new StreamWriter(saveFileDialog1.FileName))
                {
                    prevSaveDir = Path.GetDirectoryName(saveFileDialog1.FileName);
                    w.Write(newjson);                    
                }

                this.LoadFile();

                MessageBox.Show("All done!");
            }
        }
    }
}
