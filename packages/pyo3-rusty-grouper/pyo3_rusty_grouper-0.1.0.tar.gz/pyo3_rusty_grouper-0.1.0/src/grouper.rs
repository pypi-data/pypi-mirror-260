use std::path::Path;

use indicatif::{ProgressBar, ProgressStyle};

use rustc_hash::FxHashSet as HashSet;
use rustc_hash::FxHasher;
use std::fs::File;
use std::hash::{Hash, Hasher};
use std::io::{BufRead, BufReader};
use std::time::Instant;

#[derive(Eq, PartialEq, Clone, Debug)]
struct HashedUrl {
    url: String,
    hash: u64,
}

impl HashedUrl {
    fn new(url: &str) -> Self {
        let mut hasher = FxHasher::default();
        url.hash(&mut hasher);
        Self {
            url: url.to_string(),
            hash: hasher.finish(),
        }
    }
}

impl Hash for HashedUrl {
    fn hash<H: Hasher>(&self, state: &mut H) {
        self.hash.hash(state);
    }
}

impl std::borrow::Borrow<str> for HashedUrl {
    fn borrow(&self) -> &str {
        &self.url
    }
}

fn read_file(file_path: &str) -> Vec<(String, HashSet<HashedUrl>)> {
    let file_exist = Path::new(file_path).is_file();
    if !file_exist {
        panic!("File does not exist")
    }
    let file = File::open(file_path).unwrap();
    let reader = BufReader::new(file);

    let mut previous_keyword: String = String::from("");

    let mut urls_by_keywords: Vec<(String, HashSet<HashedUrl>)> = Vec::new();
    let mut group: HashSet<HashedUrl> = HashSet::default();

    for line in reader.lines() {
        let line = line.expect("Unable to read line");
        let parsed_line = line.splitn(2, ';').collect::<Vec<&str>>();
        let (keyword, url) = (parsed_line[0], parsed_line[1]);

        if !previous_keyword.is_empty() && previous_keyword != keyword {
            urls_by_keywords.push((previous_keyword, group.clone()));
            group.clear();
        }

        let hashed_url = HashedUrl::new(url);
        group.insert(hashed_url);

        previous_keyword = String::from(keyword);
    }

    println!("{}", urls_by_keywords.len());
    urls_by_keywords
}

fn group_keywords_by_urls(
    keywords_and_urls: Vec<(String, HashSet<HashedUrl>)>,
) -> Vec<Vec<String>> {
    let mut groups: Vec<Vec<String>> = Vec::new();
    let min_intersection_size = 3;
    let min_group_size = 10;
    // let mut keywords_and_urls = keywords_and_urls.clone();
    let mut keywords_and_urls = keywords_and_urls
        .into_iter()
        .map(|(keyword, urls)| (keyword, urls, false))
        .collect::<Vec<_>>();
    let start_time = Instant::now();

    let pb = ProgressBar::new(keywords_and_urls.len() as u64);
    pb.set_style(ProgressStyle::default_bar()
        .template("{spinner:.green} [{elapsed_precise}] [{bar:40.cyan/blue}] {pos}/{len} ({eta}) {msg}")
        .unwrap().progress_chars("#>-"));

    let mut outer_index: usize = 0;
    while outer_index < keywords_and_urls.len() {
        let (keyword, urls, in_group) = &keywords_and_urls[outer_index];

        let mut group = HashSet::default();
        group.insert(keyword.clone());
        let mut visited_indexes: Vec<usize> = Vec::new();

        if *in_group {
            pb.inc(1);
            outer_index += 1;
            continue;
        }
        let mut inner_index = outer_index + 1;
        while inner_index < keywords_and_urls.len() {
            let mut inner_counter = 0;
            let (keyword_1, urls_1, in_group_1) = &keywords_and_urls[inner_index];
            if *in_group_1 {
                inner_index += 1;
                continue;
            }
            for url in urls {
                if urls_1.contains(url) {
                    inner_counter += 1;
                    if inner_counter >= min_intersection_size {
                        group.insert(keyword_1.clone());
                        visited_indexes.push(inner_index);
                        break;
                    }
                }
            }
            inner_index += 1;
        }

        if group.len() >= min_group_size {
            groups.push(group.into_iter().collect());
            for index in visited_indexes {
                keywords_and_urls[index].2 = true;
            }
        }

        outer_index += 1;
        let elapsed_time = start_time.elapsed().as_secs();

        if elapsed_time > 0 {
            let speed = pb.position() / elapsed_time;
            pb.set_message(format!("{} items/sec", speed));
        }
        pb.inc(1);
    }

    pb.finish_with_message("done");

    groups
}

pub fn group_keywords(file_path: &str) -> Vec<Vec<String>> {
    let keywords_and_urls = read_file(file_path);
    let groups = group_keywords_by_urls(keywords_and_urls);

    groups
}
